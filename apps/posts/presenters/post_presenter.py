import abc
from typing import Any

from apps.posts.schemas import (CreatePostResponseSchema,
                                FeedViewPostResponseSchema)


class Presenter:
    __metaclass__ = abc.ABCMeta

    @classmethod
    def process(cls, data: Any) -> dict:
        pass


class CreatePostPresenter(Presenter):
    @classmethod
    def process(cls, data: Any = None) -> dict:
        return {'data': CreatePostResponseSchema().dump(data)}


class FeedViewPostPresenter(Presenter):
    @classmethod
    def process(cls, data: Any = None) -> dict:
        return {'data': FeedViewPostResponseSchema().dump(data, many=True)}
