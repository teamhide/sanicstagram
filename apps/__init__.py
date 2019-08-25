from apps.board.views import bp as board_v1
from sanic import Sanic


def init_listeners(app: Sanic, config):
    @app.listener('before_server_start')
    async def init_db(app, loop):
        pass

    @app.listener('after_server_stop')
    async def close_db(app, loop):
        pass


def init_blueprints(app: Sanic):
    app.blueprint(board_v1)


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
