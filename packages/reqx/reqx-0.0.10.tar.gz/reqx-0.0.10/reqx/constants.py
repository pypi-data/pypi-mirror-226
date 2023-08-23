from inspect import getfullargspec
from httpx import AsyncClient, Request

__all__ = [
    'SEND_VALID',
    'CLIENT_VALID',
    'REQUEST_STATIC',
    'REQUEST_DYNAMIC',
    'REQUEST_VALID',
]

SEND_VALID = getfullargspec(AsyncClient.send).kwonlyargs
CLIENT_VALID = getfullargspec(AsyncClient).kwonlyargs
REQUEST_STATIC = getfullargspec(Request).args + ['stream', 'extensions']
REQUEST_DYNAMIC = [k for k in getfullargspec(Request).kwonlyargs if k not in REQUEST_STATIC]
REQUEST_VALID = REQUEST_DYNAMIC + REQUEST_STATIC
