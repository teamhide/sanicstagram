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
from apps.posts.models import (Post, Attachment, Comment, Tag, PostLike)
from apps.posts.repositories import PostRepository
from apps.users.entities import UserEntity
from core.databases import session
from core.exceptions import (UploadErrorException, NotFoundErrorException,
                             CreateRowException, DeleteRowException,
                             AlreadyDoneException, UpdateRowException)


class PostUsecase:
    def __init__(self):
        self.repository = PostRepository()


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
        post = Post(
            caption=dto.caption,
            user_id=dto.user_id,
        )
        await self._process_attachments(dto=dto, post=post)
        await self._process_tags(dto=dto, post=post)

        try:
            session.add(post)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            session.rollback()
            raise UploadErrorException
        return PostEntity(
            id=post.id,
            attachments=post.attachments,
            caption=post.caption,
            creator=post.creator.nickname,
            tags=post.tags,
            comments=post.comments,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )

    async def _process_attachments(
        self,
        dto: CreatePostDto,
        post: Post,
    ) -> Optional[Post]:
        if not dto.attachments:
            return

        for attachment in dto.attachments:
            path = self._upload_attachment(attachment=attachment)
            post.attachments.append(Attachment(path=path))
        return post

    async def _process_tags(
        self,
        dto: CreatePostDto,
        post: Post,
    ) -> Optional[Post]:
        tags = self._extract_tags(caption=dto.caption)
        if not tags:
            return
        exist_tags = await self._extract_exist_tags(tags=tags)

        for tag in tags:
            if tag in exist_tags:
                exist_tag = session.query(Tag).filter(Tag.name == tag).first()
                post.tags.append(exist_tag)
            else:
                post.tags.append(Tag(name=tag))
        return post

    async def _extract_exist_tags(self, tags: List) -> List:
        tags = session.query(Tag.name).filter(Tag.name.in_(tags)).all()
        return [
            tag[0]
            for tag in tags
        ]

    async def _get_tag(self, name: str) -> bool:
        return session.query(Tag).filter(Tag.name == name).first()

    # TODO: S3에 업로드하는 코드 추가 필요
    def _upload_attachment(self, attachment) -> str:
        # 파일 객체의 실제 내용은 attachment.body에 담겨있음
        filename = uuid4().hex
        extension = attachment.name.split('.')[-1]
        return f'{filename}.{extension}'

    def _extract_tags(self, caption: str) -> List:
        pattern = r'#(\w+)'
        return re.findall(pattern=pattern, string=caption)


class LikePostUsecase(PostUsecase):
    async def execute(self, dto: LikePostDto) -> None:
        if self.repository.get_likes(post_id=dto.post_id, user_id=dto.user_id):
            raise AlreadyDoneException
        like = PostLike(
            post_id=dto.post_id,
            user_id=dto.user_id,
        )
        try:
            session.add(like)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            session.rollback()
            raise CreateRowException


class UnLikePostUsecase(PostUsecase):
    async def execute(self, dto) -> None:
        exist_like = await self.get_likes(
            post_id=dto.post_id,
            user_id=dto.user_id,
        )
        if not exist_like:
            raise AlreadyDoneException
        try:
            session.delete(exist_like)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            session.rollback()
            raise DeleteRowException


class CreateCommentUsecase(PostUsecase):
    async def execute(
        self,
        dto: CreateCommentDto,
    ) -> Union[CommentEntity, NoReturn]:
        post = session.query(Post).filter(Post.id == dto.post_id).first()
        if not post:
            raise NotFoundErrorException

        comment = Comment(
            body=dto.body,
            user_id=dto.user_id,
        )
        try:
            post.comments.append(comment)
            session.add(post)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            session.rollback()
            raise CreateRowException
        return CommentEntity(
            id=comment.id,
            body=comment.body,
            creator=comment.creator.nickname,
        )


class DeleteCommentUsecase(PostUsecase):
    async def execute(self, dto: DeleteCommentDto) -> Optional[NoReturn]:
        try:
            comment = session.query(Comment)\
                .filter(
                Comment.id == dto.comment_id,
                Comment.user_id == dto.user_id,
            ).first()
            session.delete(comment)
            session.commit()
        except UnmappedInstanceError as e:
            print(e)
            raise NotFoundErrorException
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            session.rollback()
            raise DeleteRowException


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
