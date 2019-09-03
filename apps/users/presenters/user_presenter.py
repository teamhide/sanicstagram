import abc
from typing import Any, List

from apps.users.entities import UserEntity
from apps.users.schemas import (ExploreUsersResponseSchema,
                                GetUserResponseSchema)


class Presenter:
    __metaclass__ = abc.ABCMeta

    @classmethod
    async def process(cls, data: Any) -> dict:
        pass


class RegisterUserPresenter(Presenter):
    @classmethod
    async def process(cls, data: Any) -> dict:
        pass


class GetUserListPresenter(Presenter):
    @classmethod
    async def process(cls, data: Any) -> dict:
        pass


class UpdateUserPresenter(Presenter):
    @classmethod
    async def process(cls, data: Any) -> dict:
        pass


class FollowUserPresenter(Presenter):
    @classmethod
    async def process(cls, data: Any = None) -> dict:
        return {'data': {'result': True}}


class UnFollowUserPresenter(Presenter):
    @classmethod
    async def process(cls, data: Any = None) -> dict:
        return {'data': {'result': True}}


class ExploreUsersPresenter(Presenter):
    @classmethod
    async def process(cls, data: List[UserEntity]) -> dict:
        return {'data': ExploreUsersResponseSchema().dump(data, many=True)}


class GetUserPresenter(Presenter):
    @classmethod
    async def process(cls, data: UserEntity) -> dict:
        # TODO: calculate follower/following count and apply it to response
        return {'data': GetUserResponseSchema().dump(data)}


class UserFollowersPresenter(Presenter):
    @classmethod
    async def process(cls, data: List[UserEntity]) -> dict:
        return {'data': ExploreUsersResponseSchema().dump(data, many=True)}


class UserFollowingsPresenter(Presenter):
    @classmethod
    async def process(cls, data: List[UserEntity]) -> dict:
        return {'data': ExploreUsersResponseSchema().dump(data, many=True)}


class SearchUserPresenter(Presenter):
    @classmethod
    async def process(cls, data: List[UserEntity]) -> dict:
        return {'data': ExploreUsersResponseSchema().dump(data, many=True)}
