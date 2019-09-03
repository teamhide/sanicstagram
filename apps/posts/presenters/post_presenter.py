import abc
from typing import Any

from apps.posts.schemas import (CreatePostResponseSchema,
                                FeedViewPostResponseSchema,
                                CreateCommentResponseSchema)


class Presenter:
    __metaclass__ = abc.ABCMeta

    @classmethod
    async def process(cls, data: Any) -> dict:
        pass


class CreatePostPresenter(Presenter):
    @classmethod
    async def process(cls, data: Any = None) -> dict:
        return {'data': CreatePostResponseSchema().dump(data)}


class FeedViewPostPresenter(Presenter):
    @classmethod
    async def process(cls, data: Any = None) -> dict:
        return {'data': FeedViewPostResponseSchema().dump(data, many=True)}


class CreateCommentPresenter(Presenter):
    @classmethod
    async def process(cls, data: Any = None) -> dict:
        return {'data': CreateCommentResponseSchema().dump(data)}


class DeleteCommentPresenter(Presenter):
    @classmethod
    async def process(cls, data: Any = None) -> dict:
        return {'data': {'status': True}}


class LikePostPresenter(Presenter):
    @classmethod
    async def process(cls, data: Any = None) -> dict:
        return {'data': {'status': True}}


class UnLikePostPresenter(Presenter):
    @classmethod
    async def process(cls, data: Any = None) -> dict:
        return {'data': {'status': True}}
