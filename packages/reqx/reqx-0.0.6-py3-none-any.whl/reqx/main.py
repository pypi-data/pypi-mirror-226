import asyncio
import logging.config
import platform
import random
from collections.abc import Generator
from functools import partial
from logging import getLogger, Logger
from pathlib import Path

import aiofiles
from httpx import AsyncClient, Response, Request, URL
from tqdm.asyncio import tqdm_asyncio

from .constants import *

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


async def process(fns: list[partial] | Generator[partial], desc: str = None, **kwargs) -> tuple[Response]:
    """
    Process a generator of async tasks, optionally with a progress bar.

    @param fns: List of partials or generator to process.
    @param desc: Description for tqdm progress bar. If None, no progress bar will be shown.
    @param kwargs: Keyword arguments passed to the httpx.AsyncClient.
    @return: Tuple of httpx.Response objects.
    """
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
    """
    Retry an asynchronous function with exponential backoff.

    @param fn: The async function to be retried.
    @param m: Maximum time (seconds) to wait before retrying.
    @param b: Base multiplier for the exponential backoff.
    @param max_retries: Maximum number of retries before giving up.
    @return: Return value of the 'fn' function or None if max retries is exceeded.
    """
    _kwargs = {k: v for k, v in kwargs.items() if k not in REQUEST_DYNAMIC}

    for i in range(max_retries + 1):
        try:
            r = await fn(*args, **_kwargs)
            r.raise_for_status()
            return r
        except Exception as e:
            if i == max_retries:
                logger.warning(f'Max retries exceeded\n{e}')
                return
            t = min(random.random() * (b ** i), m)
            logger.debug(f'Retrying in {f"{t:.2f}"} seconds\n{e}')
            await asyncio.sleep(t)


def build_requests(method: str, urls: list[str | URL], debug: int, **kwargs) -> Generator[Request]:
    """
    Build a generator of httpx.Request objects.

    @param method: HTTP method.
    @param urls: List of URLs.
    @param debug: If True, log the generated requests.
    @param kwargs: Keyword arguments passed to httpx.Request.
    @return: Generator of httpx.Request objects.
    """

    _kwargs = {k: v for k, v in kwargs.items() if k in REQUEST_VALID}

    def helper(d: dict) -> list[dict]:
        D = [d]
        for k, v in d.items():
            if isinstance(v, (list, range)):
                D = [{**d, k: vv} for d in D for vv in v]
        return D

    data = []
    for url in urls:
        tmp = [{'method': method, 'url': url}]
        for k, v in _kwargs.items():
            if k in REQUEST_DYNAMIC:
                cur = helper(v)
                tmp = [{**x, k: y} for x in tmp for y in cur]
            elif k in REQUEST_STATIC:
                for d in tmp:
                    d[k] = v
        data.extend(tmp)

    if debug >= 1:
        logger.debug(f'Generated {len(data)} Requests:')
    if debug >= 2:
        [logger.debug(d) for d in data]

    return (Request(**d) for d in data)


def send(method: str, urls: list[str|URL], debug: int = 0, **kwargs) -> Generator[partial]:
    """
    Build a generator of partial functions ready to send httpx.Requests.

    @param method: HTTP method (e.g. 'GET', 'POST', etc.)
    @param urls: List of URLs.
    @param debug: Verbosity level to log the generated requests.
    @param kwargs: Additional arguments for building requests and httpx send method.
    @return: Generator of partials.
    """

    async def fn(client: AsyncClient, r: dict) -> Response:
        return await backoff(client.send, r, **kwargs)

    return (partial(fn, r=r) for r in build_requests(method, urls, debug, **kwargs))


def download(urls: list[str | URL], out: str = 'out', chunk_size: int = None, **kwargs) -> Generator:
    """
    Downloads and saves large files asynchronously.

    @param urls: List of URLs.
    @param out: Directory where the downloaded files will be saved. (default: 'out')
    @param chunk_size: Number of bytes to read into memory at once. (default: None)
    @param kwargs: Additional keyword arguments to pass to the httpx.AsyncClient.stream.
    @return: Generator of partials.
    """

    async def fn(client: AsyncClient, url: str | URL) -> None:
        fname = str(url).split('/')[-1]
        async with aiofiles.open(_out / fname, 'wb') as fp:
            async with client.stream('GET', url, **kwargs) as r:
                async for chunk in r.aiter_bytes(chunk_size):
                    await fp.write(chunk)

    _out = Path(out)
    _out.mkdir(parents=True, exist_ok=True)
    return (partial(fn, url=u) for u in urls)
