# reqX

### The Efficient Web Scraping Library

A flexible interface for quickly making high volumes of asynchronous HTTP requests.

## Examples

### Run batches of async requests

These options can be passed iterables to build a request for each value.
```python
allowed = {'headers', 'params', 'cookies', 'content', 'data', 'files', 'json'}
```
E.g. pagination
```python
import asyncio
import reqx

urls = ['https://www.bcliquorstores.com/ajax/browse']
params = {'size': 24, 'page': range(2, 7), 'category': 'spirits', 'sort': 'featuredProducts:desc'}
headers = {'user-agent': '(iPhone; CPU iPhone OS 15_6 like Mac OS X)'}

res = asyncio.run(
    reqx.process(
        reqx.send('GET', urls, debug=True, params=params, headers=headers),
        http2=True,
        desc='GET'
    )
)

[print(r.json()) for r in res]
```

#### Explanation
```python
asyncio.run(
    # collect these tasks (asyncio.gather)
    reqx.process(
        # partial functions to send
        reqx.send(
            # httpx.Request configurations
            'GET',
            urls,
            params=params,
            headers=headers,
            debug=True
        ),
        # httpx.AsyncClient configurations
        http2=True,
        # add description to display a progress bar
        desc='Example GET requests'
    )
)
```

### Run batches of async downloads

```python
import asyncio
import reqx

urls = [...]

res = asyncio.run(reqx.process(
    reqx.download(urls),
    desc='Downloading files'
))
```

