from typing import Union, NoReturn

from marshmallow.exceptions import ValidationError
from sanic.request import Request
from sanic.response import json
from sanic.views import HTTPMethodView

from apps.posts.dtos import (CreatePostDto, FeedViewPostDto, CreateCommentDto,
                             DeleteCommentDto, LikePostDto, UnLikePostDto,
                             GetPostLikedUsersDto, SearchTagDto, DeletePostDto)
from apps.posts.presenters import (CreatePostPresenter, FeedViewPostPresenter,
                                   CreateCommentPresenter,
                                   DeleteCommentPresenter, LikePostPresenter,
                                   UnLikePostPresenter,
                                   GetPostLikedUsersPresenter,
                                   SearchTagPresenter, DeletePostPresenter)
from apps.posts.schemas import (CreatePostRequestSchema,
                                FeedViewPostRequestSchema,
                                CreateCommentRequestSchema,
                                DeleteCommentRequestSchema,
                                GetPostLikedUsersRequestSchema,
                                SearchTagRequestSchema)
from apps.posts.usecases import (CreatePostUsecase, FeedViewPostUsecase,
                                 CreateCommentUsecase, DeleteCommentUsecase,
                                 LikePostUsecase, UnLikePostUsecase,
                                 GetPostLikedUsersUsecase, SearchTagUsecase,
                                 DeletePostUsecase)
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
        await DeletePostUsecase().execute(
            dto=DeletePostDto(
                user_id=request['user_id'],
                post_id=post_id,
            )
        )
        response = await DeletePostPresenter.process()
        return json(body=response)


class PostList(HTTPMethodView):
    decorators = [extract_user_id_from_token()]

    async def get(self, request: Request) -> Union[json, NoReturn]:
        try:
            validator = FeedViewPostRequestSchema().load(data=request.args)
        except ValidationError:
            raise ValidationErrorException

        posts = await FeedViewPostUsecase().execute(
            dto=FeedViewPostDto(
                **validator,
                user_id=request['user_id'],
            )
        )
        response = await FeedViewPostPresenter.process(data=posts)
        return json(body=response)

    async def post(self, request: Request) -> Union[json, NoReturn]:
        try:
            validator = CreatePostRequestSchema().load(data=request.form)
        except ValidationError:
            raise ValidationErrorException

        post = await CreatePostUsecase().execute(
            dto=CreatePostDto(
                **validator,
                attachments=request.files.get('attachments'),
                user_id=request['user_id'],
            )
        )
        response = await CreatePostPresenter.process(data=post)
        return json(body=response)


class LikePost(HTTPMethodView):
    decorators = [extract_user_id_from_token()]

    async def post(
        self,
        request: Request,
        post_id: int,
    ) -> Union[json, NoReturn]:
        await LikePostUsecase().execute(
            dto=LikePostDto(
                user_id=request['user_id'],
                post_id=post_id,
            )
        )
        response = await LikePostPresenter.process()
        return json(body=response)


class UnLikePost(HTTPMethodView):
    decorators = [extract_user_id_from_token()]

    async def post(
        self,
        request: Request,
        post_id: int,
    ) -> Union[json, NoReturn]:
        await UnLikePostUsecase().execute(
            dto=UnLikePostDto(
                user_id=request['user_id'],
                post_id=post_id,
            )
        )
        response = await UnLikePostPresenter.process()
        return json(body=response)


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

        comment = await CreateCommentUsecase().execute(
            dto=CreateCommentDto(
                **validator,
                post_id=post_id,
                user_id=request['user_id'],
            ),
        )
        response = await CreateCommentPresenter.process(data=comment)
        return json(body=response)

    async def delete(
        self,
        request: Request,
        post_id: int,
        comment_id: int,
    ) -> Union[json, NoReturn]:
        try:
            validator = DeleteCommentRequestSchema().load(
                data={'post_id': post_id, 'comment_id': comment_id},
            )
        except ValidationError as e:
            print(e)
            raise ValidationErrorException

        await DeleteCommentUsecase().execute(
            dto=DeleteCommentDto(**validator, user_id=request['user_id']),
        )
        response = await DeleteCommentPresenter.process()
        return json(body=response)


class SearchPost(HTTPMethodView):
    decorators = [extract_user_id_from_token()]

    async def get(
        self,
        request: Request,
        user_id: int,
    ) -> Union[json, NoReturn]:
        pass


class SearchTag(HTTPMethodView):
    decorators = [extract_user_id_from_token()]

    async def get(self, request: Request) -> Union[json, NoReturn]:
        try:
            validator = SearchTagRequestSchema().load(data=request.args)
        except ValidationError as e:
            print(e)
            raise ValidationErrorException

        posts = await SearchTagUsecase().execute(
            dto=SearchTagDto(**validator, user_id=request['user_id']),
        )
        response = await SearchTagPresenter.process(data=posts)
        return json(body=response)


class GetPostLikedUsers(HTTPMethodView):
    decorators = [extract_user_id_from_token()]

    async def get(
        self,
        request: Request,
        post_id: int,
    ) -> Union[json, NoReturn]:
        try:
            validator = GetPostLikedUsersRequestSchema().load(
                data=request.args,
            )
        except ValidationError as e:
            print(e)
            raise ValidationErrorException

        users = await GetPostLikedUsersUsecase().execute(
            dto=GetPostLikedUsersDto(
                **validator,
                user_id=request['user_id'],
                post_id=post_id,
            ),
        )
        response = await GetPostLikedUsersPresenter.process(data=users)
        return json(body=response)
