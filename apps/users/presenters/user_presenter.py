import abc
from typing import Any, List

from apps.users.entities import UserEntity
from apps.users.schemas import ExploreUsersResponseSchema


class Presenter:
    __metaclass__ = abc.ABCMeta

    @classmethod
    def process(cls, data: Any):
        pass


class RegisterUserPresenter(Presenter):
    @classmethod
    def process(cls, data: Any):
        pass


class GetUserListPresenter(Presenter):
    @classmethod
    def process(cls, data: Any):
        pass


class UpdateUserPresenter(Presenter):
    @classmethod
    def process(cls, data: Any):
        pass


class FollowUserPresenter(Presenter):
    @classmethod
    def process(cls, data: Any):
        pass


class UnFollowUserPresenter(Presenter):
    @classmethod
    def process(cls, data: Any):
        pass


class ExploreUsersPresenter(Presenter):
    @classmethod
    def process(cls, data: List[UserEntity]):
        return {'data': ExploreUsersResponseSchema().dump(data, many=True)}
