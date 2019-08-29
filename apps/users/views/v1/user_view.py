from typing import Union, NoReturn

from marshmallow.exceptions import ValidationError
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from apps.users.dtos import (FollowUserDto, UnFollowUserDto)
from apps.users.schemas import (FollowUserRequestSchema,
                                UnFollowUserRequestSchema)
from apps.users.usecases import (FollowUserUsecase, UnFollowUserUsecase,
                                 ExploreUsersUsecase)
from apps.users.presenters import ExploreUsersPresenter
from core.decorators import extract_user_id_from_token
from core.exceptions import ValidationErrorException


class User(HTTPMethodView):
    decorators = []

    async def get(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        pass

    async def post(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        pass


class UserList(HTTPMethodView):
    decorators = []

    async def get(self, request: Request) -> Union[json, NoReturn]:
        return json(body={'result': True})

    async def post(self, request: Request) -> Union[json, NoReturn]:
        pass


class FollowUser(HTTPMethodView):
    decorators = [extract_user_id_from_token()]

    async def post(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        try:
            validator = FollowUserRequestSchema().load(
                data={
                    'user_id': request['user_id'],
                    'follow_user_id': user_id,
                },
            )
        except ValidationError:
            raise ValidationErrorException

        FollowUserUsecase().execute(dto=FollowUserDto(**validator))
        return json(body={'result': True})


class UnFollowUser(HTTPMethodView):
    decorators = [extract_user_id_from_token()]

    async def post(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        try:
            validator = UnFollowUserRequestSchema().load(
                data={
                    'user_id': request['user_id'],
                    'follow_user_id': user_id,
                },
            )
        except ValidationError:
            raise ValidationErrorException

        UnFollowUserUsecase().execute(dto=UnFollowUserDto(**validator))
        return json(body={'result': True})


class ExploreUsers(HTTPMethodView):
    decorators = []

    async def get(self, request: Request) -> Union[json, NoReturn]:
        users = ExploreUsersUsecase().execute()
        response = ExploreUsersPresenter.process(data=users)
        return json(body=response)


class UserFollowers(HTTPMethodView):
    decorators = []

    async def get(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        pass


class UserFollowings(HTTPMethodView):
    decorators = []

    async def get(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        pass


class Login(HTTPMethodView):
    decorators = []

    async def post(self, request: Request) -> Union[json, NoReturn]:
        pass
