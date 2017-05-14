# _*_ coding: utf-8 _*_

"""
@file: request.py
@time: 2017/5/2 下午3:56
@author: pigbreeder
"""
import collections


# Response = collections.namedtuple('Response', ['header', 'data', 'meta'])


class Request():
    GET = 'GET'
    POST = 'POST'

    def __init__(self, url, callback=None, method='GET', headers=None, body=None,
                 cookies=None, meta=None, encoding='utf-8', priority=0,
                 dont_filter=False, errback=None, flags=None):
        self._encoding = encoding  # this one has to be set first
        self.method = str(method).upper()
        self.url = url
        self.body = body or {}
        self.retry = 0
        assert isinstance(priority, int), "Request priority not an integer: %r" % priority
        self.priority = priority

        assert callback or not errback, "Cannot use errback without a callback"
        self.callback = callback
        self.errback = errback

        self.cookies = cookies or {}
        self.headers = headers or {}
        self.dont_filter = dont_filter

        self.meta = dict(meta) if meta else None
        self.flags = [] if flags is None else list(flags)

    def __str__(self):
        return "<%s %s>" % (self.method, self.url)

    __repr__ = __str__

    def copy(self):
        """Return a copy of this Request"""
        return self.replace()

    def replace(self, *args, **kwargs):

        for x in ['url', 'method', 'headers', 'body', 'cookies', 'meta', 'retry',
                  'encoding', 'priority', 'dont_filter', 'callback', 'errback']:
            kwargs.setdefault(x, getattr(self, x))
        cls = kwargs.pop('cls', self.__class__)
        return cls(*args, **kwargs)

    @staticmethod
    def unserialize(*args, **kwargs):

        for x in ['url', 'method', 'headers', 'body', 'cookies', 'meta', 'retry',
                  'encoding', 'priority', 'dont_filter', 'callback', 'errback']:
            kwargs.setdefault(x, None)
        cls = kwargs.pop('cls', Request.__class__)
        return cls(*args, **kwargs)

    def serialize(self, *args, **kwargs):

        for x in ['url', 'method', 'headers', 'body', 'cookies', 'meta', 'retry',
                  'encoding', 'priority', 'dont_filter', 'callback', 'errback']:
            kwargs.setdefault(x, getattr(self, x))
        kwargs.pop('cls', Request.__class__)
        return kwargs


class Response():
    def __init__(self, url, status=200, headers=None, body=None, flags=None, request=None):
        self.headers = headers or {}
        self.status = int(status)
        self.body = body
        self.url = url
        self.request = request
        self.flags = [] if flags is None else list(flags)

    @property
    def meta(self):
        try:
            return self.request.meta
        except AttributeError:
            raise AttributeError(
                "Response.meta not available, this response "
                "is not tied to any request"
            )

    def __str__(self):
        return "<%d %s>" % (self.status, self.url)

    __repr__ = __str__

    def copy(self):
        """Return a copy of this Response"""
        return self.replace()

    def replace(self, *args, **kwargs):
        """Create a new Response with the same attributes except for those
        given new values.
        """
        for x in ['url', 'status', 'headers', 'body', 'request', 'flags']:
            kwargs.setdefault(x, getattr(self, x))
        cls = kwargs.pop('cls', self.__class__)
        return cls(*args, **kwargs)
