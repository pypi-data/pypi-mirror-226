REQUEST_DYNAMIC = {'headers', 'params', 'cookies', 'content', 'data', 'files', 'json'}
REQUEST_STATIC = {'method', 'url', 'stream', 'extensions'}
REQUEST_VALID = REQUEST_DYNAMIC | REQUEST_STATIC
