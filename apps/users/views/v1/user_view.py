from typing import Union, NoReturn

from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView


class User(HTTPMethodView):
    decorators = []

    async def get(self, request: Request) -> Union[json, NoReturn]:
        pass

    async def post(self, request: Request) -> Union[json, NoReturn]:
        pass


class UserList(HTTPMethodView):
    decorators = []

    async def get(self, request: Request) -> Union[json, NoReturn]:
        return json(body={'result': True})

    async def post(self, request: Request) -> Union[json, NoReturn]:
        pass
