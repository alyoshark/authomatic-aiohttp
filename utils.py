from urllib.parse import parse_qsl

from authomatic.adapters import BaseAdapter


class AioAdapter(BaseAdapter):
    def __init__(self, request, response):
        self.request = request
        self.response = response

    @property
    def url(self):
        return "%s://%s%s" % (
            self.request.scheme,
            self.request.host,
            self.request.path,
        )

    @property
    def params(self):
        return dict(parse_qsl(self.request.query_string))

    @property
    def cookies(self):
        return self.request.cookies

    def write(self, value):
        self.response.write(value)

    def set_header(self, key, value):
        self.response.headers.add(key, value)

    def set_status(self, status):
        status = status[:3]
        self.response.set_status(status)
