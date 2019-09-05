from typing import Union, NoReturn

from marshmallow.exceptions import ValidationError
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from apps.users.dtos import (FollowUserDto, UnFollowUserDto, GetUserDto)
from apps.users.presenters import (ExploreUsersPresenter, GetUserPresenter,
                                   UserFollowersPresenter, FollowUserPresenter,
                                   UnFollowUserPresenter,
                                   UserFollowingsPresenter,
                                   SearchUserPresenter)
from apps.users.schemas import GetUserRequestSchema, SearchUserRequestSchema
from apps.users.usecases import (FollowUserUsecase, UnFollowUserUsecase,
                                 ExploreUsersUsecase, GetUserUsecase,
                                 GetUserFollowersUsecase,
                                 GetUserFollowingsUsecase, SearchUserUsecase)
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
        await FollowUserUsecase().execute(
            dto=FollowUserDto(
                user_id=request['user_id'],
                follow_user_id=user_id,
            )
        )
        response = await FollowUserPresenter.process()
        return json(body=response)


class UnFollowUser(HTTPMethodView):
    decorators = [extract_user_id_from_token()]

    async def post(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        await UnFollowUserUsecase().execute(
            dto=UnFollowUserDto(
                user_id=request['user_id'],
                follow_user_id=user_id,
            )
        )
        response = await UnFollowUserPresenter.process()
        return json(body=response)


class ExploreUsers(HTTPMethodView):
    decorators = [extract_user_id_from_token()]

    async def get(self, request: Request) -> Union[json, NoReturn]:
        users = await ExploreUsersUsecase().execute()
        response = await ExploreUsersPresenter.process(data=users)
        return json(body=response)


class UserFollowers(HTTPMethodView):
    decorators = [extract_user_id_from_token()]

    async def get(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        followers = await GetUserFollowersUsecase().execute(user_id=user_id)
        response = await UserFollowersPresenter.process(data=followers)
        return json(body=response)


class UserFollowings(HTTPMethodView):
    decorators = [extract_user_id_from_token()]

    async def get(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        followings = await GetUserFollowingsUsecase().execute(user_id=user_id)
        response = await UserFollowingsPresenter.process(data=followings)
        return json(body=response)


class Login(HTTPMethodView):
    decorators = []

    async def post(self, request: Request) -> Union[json, NoReturn]:
        pass


class UserProfile(HTTPMethodView):
    decorators = []

    async def get(
        self,
        request: Request,
        nickname: str,
    ) -> Union[json, NoReturn]:
        try:
            validator = GetUserRequestSchema().load(
                data={'nickname': nickname},
            )
        except ValidationError:
            raise ValidationErrorException

        user = await GetUserUsecase().execute(dto=GetUserDto(**validator))
        response = await GetUserPresenter.process(data=user)
        return json(body=response)


class SearchUser(HTTPMethodView):
    decorators = []

    async def get(
        self,
        request: Request,
        nickname: str,
    ) -> Union[json, NoReturn]:
        try:
            SearchUserRequestSchema().load(data={'nickname': nickname})
        except ValidationError:
            raise ValidationErrorException

        users = await SearchUserUsecase().execute(nickname=nickname)
        response = await SearchUserPresenter.process(data=users)
        return json(body=response)
