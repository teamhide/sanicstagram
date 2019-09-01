from typing import Union, NoReturn

from marshmallow.exceptions import ValidationError
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from apps.posts.dtos import CreatePostDto
from apps.posts.presenters import CreatePostPresenter
from apps.posts.schemas import CreatePostSchema
from apps.posts.usecases import CreatePostUsecase
from core.exceptions import ValidationErrorException
from core.decorators import extract_user_id_from_token


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
        pass

    async def post(self, request: Request) -> Union[json, NoReturn]:
        try:
            validator = CreatePostSchema().load(data=request.form)
        except ValidationError:
            raise ValidationErrorException

        CreatePostUsecase().execute(
            dto=CreatePostDto(
                **validator,
                attachments=request.files['attachments'],
                user_id=request['user_id'],
            )
        )
        response = CreatePostPresenter.process()
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
    decorators = []

    async def get(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        pass


class SearchPost(HTTPMethodView):
    decorators = []

    async def get(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        pass
