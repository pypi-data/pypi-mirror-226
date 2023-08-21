import asyncio
import logging.config
import platform
import random
from functools import partial
from logging import getLogger, Logger
from pathlib import Path
from typing import Generator

import aiofiles
from httpx import AsyncClient, Response
from tqdm.asyncio import tqdm_asyncio

try:
    if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
        import nest_asyncio

        nest_asyncio.apply()
except:
    ...

if platform.system() in {'Darwin', 'Linux'}:
    try:
        import uvloop

        uvloop.install()
    except ImportError as e:
        ...

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {'standard': {'format': '%(asctime)s.%(msecs)03d [%(levelname)s] :: %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}},
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'level': 'DEBUG', 'formatter': 'standard', 'stream': 'ext://sys.stdout'},
        'file': {'class': 'logging.FileHandler', 'level': 'DEBUG', 'formatter': 'standard', 'filename': 'log.log', 'mode': 'a'},
    },
    'loggers': {'my_logger': {'handlers': ['console', 'file'], 'level': 'DEBUG'}}
})
logger = getLogger(list(Logger.manager.loggerDict)[-1])


async def process(fns: list[partial] | Generator, desc: str = None, **kwargs) -> tuple[Response]:
    # always override default httpx.AsyncClient headers
    default_config = {
        'headers': {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/112.0.0.0'}
    }
    async with AsyncClient(**(default_config | kwargs)) as client:
        tasks = (fn(client=client) for fn in fns)
        if desc:
            return await tqdm_asyncio.gather(*tasks, desc=desc)
        return await asyncio.gather(*tasks)


async def backoff(fn: callable, *args, m: int = 20, b: int = 2, max_retries: int = 8, **kwargs) -> any:
    """Async Exponential Backoff"""
    for i in range(max_retries + 1):
        try:
            r = await fn(*args, **kwargs)
            r.raise_for_status()
            return r
        except Exception as e:
            if i == max_retries:
                logger.warning(f'Max retries exceeded\n{e}')
                return
            t = min(random.random() * (b ** i), m)
            logger.debug(f'Retrying in {f"{t:.2f}"} seconds\n{e}')
            await asyncio.sleep(t)


def get(urls: list[str], **kwargs) -> Generator:
    """
    Convenience method for making simple GET requests
    """

    async def fn(client: AsyncClient, url: str) -> Response:
        return await backoff(client.get, url, **kwargs)

    return (partial(fn, url=u) for u in urls)


def download(urls: list[str], out: str = 'out', chunk_size: int = None, **kwargs) -> Generator:
    """
    Convenience method for downloading/saving large files
    """

    async def fn(client: AsyncClient, url: str) -> None:
        fname = url.split('/')[-1]
        async with aiofiles.open(_out / fname, 'wb') as fp:
            async with client.stream('GET', url, **kwargs) as r:
                async for chunk in r.aiter_bytes(chunk_size):
                    await fp.write(chunk)

    _out = Path(out)
    _out.mkdir(parents=True, exist_ok=True)
    return (partial(fn, url=u) for u in urls)


def send(method: str, cfgs: list[dict] = None, **kwargs) -> Generator:
    """
    Generic method to make network requests
    """

    async def fn(client: AsyncClient, cfg: dict) -> Response:
        return await backoff(client.request, method, **cfg, **kwargs)

    return (partial(fn, cfg=cfg) for cfg in cfgs)
