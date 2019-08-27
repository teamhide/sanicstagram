import abc
from typing import Any


class Presenter:
    __metaclass__ = abc.ABCMeta

    @classmethod
    def process(cls, response: Any):
        pass


class RegisterUserPresenter(Presenter):
    @classmethod
    def process(cls, response: Any):
        pass


class GetUserListPresenter(Presenter):
    @classmethod
    def process(cls, response: Any):
        pass


class UpdateUserPresenter(Presenter):
    @classmethod
    def process(cls, response: Any):
        pass


class FollowUserPresenter(Presenter):
    @classmethod
    def process(cls, response: Any):
        pass


class UnFollowUserPresenter(Presenter):
    @classmethod
    def process(cls, response: Any):
        pass
