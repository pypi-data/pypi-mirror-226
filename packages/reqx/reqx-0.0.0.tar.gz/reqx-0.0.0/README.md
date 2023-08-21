# reqX

### The Efficient Web Scraping Library

A simple interface for quickly making asynchronous HTTP requests and parsing data.

## Examples

### GET

```python
import asyncio
import reqx

urls = [...]

res = asyncio.run(reqx.process(
    reqx.get(urls),
    desc='example requests'
))
```

### Download

```python
import asyncio
import reqx

urls = [...]

res = asyncio.run(reqx.process(
    reqx.download(urls),
    desc='downloading files'
))
```

### GET: additional configuration

```python
import asyncio
import httpx
import reqx

# define the requests to make as a list of dicts. They keys correspond to `httpx.AsyncClient` parameters
cfgs = [
    {
        'url': 'https://www.bcliquorstores.com/ajax/browse',
        'headers': {'user-agent': '(iPhone; CPU iPhone OS 15_6 like Mac OS X)'},
        'cookies': None,
        'params': {'size': 24, 'page': i, 'category': 'spirits', 'sort': 'featuredProducts:desc'}
    }
    for i in range(10)
]

res = asyncio.run(reqx.process(
    reqx.send('GET', cfgs),
    http2=True,
    limits=httpx.Limits(max_connections=1000, max_keepalive_connections=50),
    desc='example requests'
))
```
