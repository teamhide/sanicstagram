from typing import Union, NoReturn

from marshmallow.exceptions import ValidationError
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView


class Post(HTTPMethodView):
    decorators = []

    async def get(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        pass


class LikePost(HTTPMethodView):
    decorators = []

    async def get(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        pass


class UnLikePost(HTTPMethodView):
    decorators = []

    async def get(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        pass


class Comment(HTTPMethodView):
    decorators = []

    async def get(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        pass


class SearchPost(HTTPMethodView):
    decorators = []

    async def get(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        pass


class PostDetail(HTTPMethodView):
    decorators = []

    async def get(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        pass
