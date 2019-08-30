from apps.board.views import bp as board_v1
from apps.users.views import bp as users_v1
from apps.posts.views import bp as posts_v1
from apps.home.views import bp as home
from sanic import Sanic
from core.databases import session


def init_listeners(app: Sanic, config):
    @app.listener('before_server_start')
    async def init_db(app, loop):
        pass

    @app.listener('after_server_stop')
    async def close_db(app, loop):
        pass

    @app.middleware('request')
    async def print_on_request(request):
        pass

    @app.middleware('response')
    async def close_session(request, response):
        session.close()


def init_blueprints(app: Sanic):
    app.blueprint(home)
    app.blueprint(board_v1)
    app.blueprint(users_v1)
    app.blueprint(posts_v1)


def init_middlewares(app: Sanic, config):
    pass


def init_exception_handlers(app: Sanic, config):
    pass


def create_app(config):
    app = Sanic(__name__)

    init_listeners(app=app, config=config)
    init_blueprints(app=app)
    init_middlewares(app=app, config=config)
    init_exception_handlers(app=app, config=config)

    return app
