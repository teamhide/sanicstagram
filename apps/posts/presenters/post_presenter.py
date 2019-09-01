import abc
from typing import Any
from apps.posts.schemas import CreatePostResponseSchema


class Presenter:
    __metaclass__ = abc.ABCMeta

    @classmethod
    def process(cls, data: Any) -> dict:
        pass


class CreatePostPresenter(Presenter):
    @classmethod
    def process(cls, data: Any = None) -> dict:
        return {'data': CreatePostResponseSchema().dump(data)}
