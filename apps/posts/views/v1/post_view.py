from typing import Union, NoReturn

from marshmallow.exceptions import ValidationError
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from apps.posts.dtos import (CreatePostDto, FeedViewPostDto, CreateCommentDto)
from apps.posts.presenters import (CreatePostPresenter, FeedViewPostPresenter,
                                   CreateCommentPresenter)
from apps.posts.schemas import (CreatePostRequestSchema,
                                FeedViewPostRequestSchema,
                                CreateCommentRequestSchema)
from apps.posts.usecases import (CreatePostUsecase, FeedViewPostUsecase,
                                 CreateCommentUsecase)
from core.decorators import extract_user_id_from_token
from core.exceptions import ValidationErrorException


class Post(HTTPMethodView):
    decorators = [extract_user_id_from_token()]

    async def get(
        self,
        request: Request,
        post_id: int,
    ) -> Union[json, NoReturn]:
        pass

    async def put(
        self,
        request: Request,
        post_id: int,
    ) -> Union[json, NoReturn]:
        pass

    async def delete(
        self,
        request: Request,
        post_id: int,
    ) -> Union[json, NoReturn]:
        pass


class PostList(HTTPMethodView):
    decorators = [extract_user_id_from_token()]

    async def get(self, request: Request) -> Union[json, NoReturn]:
        try:
            validator = FeedViewPostRequestSchema().load(data=request.args)
        except ValidationError:
            raise ValidationErrorException

        posts = FeedViewPostUsecase().execute(
            dto=FeedViewPostDto(
                **validator,
                user_id=request['user_id'],
            )
        )
        response = FeedViewPostPresenter.process(data=posts)
        return json(body=response)

    async def post(self, request: Request) -> Union[json, NoReturn]:
        try:
            validator = CreatePostRequestSchema().load(data=request.form)
        except ValidationError:
            raise ValidationErrorException

        post = CreatePostUsecase().execute(
            dto=CreatePostDto(
                **validator,
                attachments=request.files.get('attachments'),
                user_id=request['user_id'],
            )
        )
        response = CreatePostPresenter.process(data=post)
        return json(body=response)


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
    decorators = [extract_user_id_from_token()]

    async def post(
        self,
        request: Request,
        post_id: int,
    ) -> Union[json, NoReturn]:
        try:
            validator = CreateCommentRequestSchema().load(data=request.form)
        except ValidationError as e:
            print(e)
            raise ValidationErrorException

        comment = CreateCommentUsecase().execute(
            dto=CreateCommentDto(
                **validator,
                post_id=post_id,
                user_id=request['user_id'],
            ),
        )
        response = CreateCommentPresenter.process(data=comment)
        return json(body=response)


class SearchPost(HTTPMethodView):
    decorators = []

    async def get(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        pass
