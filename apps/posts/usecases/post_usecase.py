import re
from typing import List, Union, NoReturn, Optional
from uuid import uuid4

import sqlalchemy.exc
import sqlalchemy.orm
from sqlalchemy.orm.exc import UnmappedInstanceError

from apps.posts.dtos import (CreatePostDto, FeedViewPostDto, CreateCommentDto,
                             DeleteCommentDto, LikePostDto,
                             GetPostLikedUsersDto, SearchTagDto, DeletePostDto,
                             GetPostDto, UpdatePostDto)
from apps.posts.entities import PostEntity, CommentEntity
from apps.posts.enum import DefaultPaging
from apps.posts.models import (Post, Comment, Tag, PostLike)
from apps.posts.repositories import PostPSQLRepository
from apps.users.entities import UserEntity
from core.databases import session
from core.exceptions import (NotFoundErrorException,
                             CreateRowException, DeleteRowException,
                             AlreadyDoneException, UpdateRowException)


class PostUsecase:
    def __init__(self):
        self.repository = PostPSQLRepository()


class GetPostDetailUsecase(PostUsecase):
    async def execute(self, dto: GetPostDto) -> Union[PostEntity, NoReturn]:
        post_entity = self.repository.get_post(post_id=dto.post_id)
        if not post_entity:
            raise NotFoundErrorException

        post_entity.is_liked = True if self.repository.get_likes(post_id=dto.post_id, user_id=dto.user_id) else False  # noqa
        return post_entity


class FeedViewPostUsecase(PostUsecase):
    async def execute(self, dto: FeedViewPostDto) -> List[PostEntity]:
        return self.repository.get_post_list(
            user_id=dto.user_id,
            prev=dto.prev,
            limit=dto.limit,
            order=True,
        )


class CreatePostUsecase(PostUsecase):
    async def execute(self, dto: CreatePostDto) -> Union[PostEntity, NoReturn]:
        post_entity = PostEntity(
            caption=dto.caption,
            user_id=dto.user_id,
        )
        if dto.attachments:
            post_entity.attachments = await self._process_attachments(
                attachments=dto.attachments['attachments'],
            )

        tags = self._extract_tags(caption=dto.caption)
        if tags:
            post_entity.tags = tags

        return self.repository.save_post(post_entity=post_entity)

    async def _process_attachments(self, attachments: List) -> List:
        return [
            self._upload_attachment(attachment=attachment)
            for attachment in attachments
        ]

    # TODO: S3에 업로드하는 코드 추가 필요
    def _upload_attachment(self, attachment) -> str:
        # 파일 객체의 실제 내용은 attachment.body에 담겨있음
        return self._encrypt_filename(attachment=attachment)

    def _encrypt_filename(self, attachment) -> str:
        extension = attachment.name.split('.')[-1]
        return f'{uuid4().hex}.{extension}'

    def _extract_tags(self, caption: str) -> List:
        pattern = r'#(\w+)'
        return re.findall(pattern=pattern, string=caption)


class LikePostUsecase(PostUsecase):
    async def execute(self, dto: LikePostDto) -> None:
        if self.repository.get_like(post_id=dto.post_id, user_id=dto.user_id):
            raise AlreadyDoneException

        self.repository.like_post(post_id=dto.post_id, user_id=dto.user_id)


class UnLikePostUsecase(PostUsecase):
    async def execute(self, dto) -> None:
        exist_like = await self.repository.get_like(
            post_id=dto.post_id,
            user_id=dto.user_id,
        )
        if not exist_like:
            raise AlreadyDoneException

        self.repository.unlike_post(post_id=dto.post_id, user_id=dto.user_id)


class CreateCommentUsecase(PostUsecase):
    async def execute(
        self,
        dto: CreateCommentDto,
    ) -> Union[CommentEntity, NoReturn]:
        post = self.repository.get_post(post_id=dto.post_id)
        if not post:
            raise NotFoundErrorException

        return self.repository.save_comment(
            post_id=dto.post_id,
            body=dto.body,
            user_id=dto.user_id,
        )


class DeleteCommentUsecase(PostUsecase):
    async def execute(self, dto: DeleteCommentDto) -> Optional[NoReturn]:
        self.repository.delete_comment(
            comment_id=dto.comment_id,
            user_id=dto.user_id,
        )


class SearchPostUsecase(PostUsecase):
    async def execute(self, dto) -> PostEntity:
        pass


class GetPostLikedUsersUsecase(PostUsecase):
    async def execute(self, dto: GetPostLikedUsersDto) -> List[UserEntity]:
        query = session.query(PostLike)\
            .filter(
            PostLike.post_id == dto.post_id,
            PostLike.user_id == dto.user_id,
        )
        if dto.prev:
            query = query.filter(PostLike.id > dto.prev)
        if dto.limit and dto.limit < DefaultPaging.LIMIT.value:
            query = query.limit(dto.limit)
        else:
            query = query.limit(DefaultPaging.LIMIT.value)
        post_like = query.all()

        return [
            UserEntity(
                id=like.user.id,
                nickname=like.user.nickname,
                profile_image=like.user.profile_image,
                bio=like.user.bio,
                website=like.user.website,
            )
            for like in post_like
        ]


class SearchTagUsecase(PostUsecase):
    async def execute(self, dto: SearchTagDto) -> List[PostEntity]:
        query = session.query(Post).filter(Tag.name.in_([dto.tag]))\
            .order_by(Post.id.desc())
        if dto.prev:
            query = query.filter(Post.id > dto.prev)
        if dto.limit and dto.limit < DefaultPaging.LIMIT.value:
            query = query.limit(DefaultPaging.LIMIT.value)
        posts = query.all()

        return [
            PostEntity(
                id=post.id,
                attachments=post.attachments,
                caption=post.caption,
                creator=post.creator.nickname,
                tags=post.tags,
                comments=post.comments,
                created_at=post.created_at,
                updated_at=post.updated_at,
            )
            for post in posts
        ]


class DeletePostUsecase(PostUsecase):
    async def execute(self, dto: DeletePostDto) -> Optional[NoReturn]:
        post = session.query(Post)\
            .filter(
            Post.id == dto.post_id,
            Post.user_id == dto.user_id,
        ).first()
        if not post:
            raise NotFoundErrorException

        try:
            session.delete(post)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            raise DeleteRowException


class UpdatePostUsecase(PostUsecase):
    async def execute(self, dto: UpdatePostDto) -> Optional[NoReturn]:
        post = session.query(Post)\
            .filter(
            Post.id == dto.post_id,
            Post.user_id == dto.user_id,
        ).first()
        if not post:
            raise NotFoundErrorException

        await self._process_update_post(post=post, dto=dto)

        try:
            session.add(post)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            session.rollback()
            raise UpdateRowException

    async def _process_update_post(
        self,
        post: Post,
        dto: UpdatePostDto,
    ) -> None:
        if dto.reuse_attachment_id:
            pass
        if dto.attachments:
            pass
        if dto.caption:
            post.caption = dto.caption
