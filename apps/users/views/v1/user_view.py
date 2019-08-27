from typing import Union, NoReturn

from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

# from apps.users.dtos import FollowUserDto
from apps.users.schemas import (FollowUserRequestSchema,
                                UnFollowUserRequestSchema)
from core.exceptions import ValidationErrorException


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


class FollowUser(HTTPMethodView):
    decorators = []

    async def get(self, request: Request) -> Union[json, NoReturn]:
        validator = FollowUserRequestSchema().load(data=request.form)
        if validator.errors:
            raise ValidationErrorException


class UnFollowUser(HTTPMethodView):
    decorators = []

    async def get(self, request: Request) -> Union[json, NoReturn]:
        validator = UnFollowUserRequestSchema().load(data=request.form)
        if validator.errors:
            raise ValidationErrorException


class ExploreUsers(HTTPMethodView):
    decorators = []

    async def get(self, request: Request) -> Union[json, NoReturn]:
        pass


class UserFollowers(HTTPMethodView):
    decorators = []

    async def get(self, request: Request) -> Union[json, NoReturn]:
        pass


class UserFollowings(HTTPMethodView):
    decorators = []

    async def get(self, request: Request) -> Union[json, NoReturn]:
        pass


class Login(HTTPMethodView):
    decorators = []

    async def post(self, request: Request) -> Union[json, NoReturn]:
        pass
