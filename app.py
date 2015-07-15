import asyncio
from asyncio import coroutine

from aiohttp import web
from aiohttp_session import get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

import ujson as json
from authomatic import Authomatic

from utils import AioAdapter, login_user, login_required
import config


authomatic = Authomatic(config.OAUTH_CONFIG, str(config.SECRET))


@coroutine
def login(request):
    provider = request.match_info.get('provider', 'fb')
    response = web.Response()
    result = authomatic.login(AioAdapter(request, response), provider)
    if result and result.user:
        result.user.update()
        user_obj = result.user
        provider_id = "%s:%s" % (provider, user_obj.id)
        email = user_obj.email
        gender = int(user_obj.gender == 'male') # 1 for male and 0 for female
        firstname = user_obj.first_name
        fullname = user_obj.name
        print(provider_id, email, gender, fullname)
        yield from login_user(request, provider_id)
        response.body = b"Hello world"
    return response


@coroutine
@login_required
def secret(request):
    ''' My awesome login demo '''
    return web.Response(body=b'Some secret')


@coroutine
def init(loop):
    app = web.Application(
        # loop=loop,
        middlewares=[session_middleware(EncryptedCookieStorage(config.SECRET))],
    )
    app.router.add_route('GET', '/login/{provider}', login)
    app.router.add_route('GET', '/secret', secret)
    srv = yield from loop.create_server(
        app.make_handler(),
        'auth.xchtest.com',
        8080,
    )
    print("Server started")
    return srv


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()
