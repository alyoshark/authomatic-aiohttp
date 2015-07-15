from urllib.parse import parse_qsl
from asyncio import coroutine

from authomatic.adapters import BaseAdapter

from aiohttp import web
from aiohttp_session import get_session


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


@coroutine
def login_user(request, provider_id):
    session = yield from get_session(request)
    session['provider_id'] = provider_id
    # session[provider_id] = User.get_uid(provider_id)
    session[provider_id] = User.get_uid(provider_id)


def login_required(func):
    def wrapper(request):
        session = yield from get_session(request)
        provider_id = session.get('provider_id')
        if provider_id:
            uid = session.get(provider_id)
            # if uid and uid == User.get_uid(provider_id):
            if uid and uid == provider_id:
                return func(request)
        return web.Response(body=b'Not logged in')
    return wrapper
