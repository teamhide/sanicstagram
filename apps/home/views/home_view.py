from typing import Union, NoReturn

from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView


class Home(HTTPMethodView):
    decorators = []

    async def get(self, request: Request) -> Union[json, NoReturn]:
        return json({'statue': True})
