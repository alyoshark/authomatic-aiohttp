import asyncio
from asyncio import coroutine

from aiohttp import web
import ujson as json
from authomatic import Authomatic

from utils import AioAdapter
import config


authomatic = Authomatic(config.OAUTH_CONFIG, 'supersecretkey')


@coroutine
def login(request):
    provider = request.match_info.get('provider', 'fb')
    response = web.Response()
    result = authomatic.login(AioAdapter(request, response), provider)
    if result:
        if result.user:
            result.user.update()
            response.body = str(user)
    return response


@coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/login/{provider}', login)
    srv = yield from loop.create_server(
        app.make_handler(),
        'auth.logintest.com',
        8080,
    )
    print("Server started")
    return srv


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()
