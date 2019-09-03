import re
from typing import List, Union, NoReturn, Optional
from uuid import uuid4

import sqlalchemy.exc
import sqlalchemy.orm
from sqlalchemy.orm.exc import UnmappedInstanceError

from apps.posts.dtos import (CreatePostDto, FeedViewPostDto, CreateCommentDto,
                             DeleteCommentDto)
from apps.posts.entities import PostEntity, CommentEntity
from apps.posts.models import (Post, Attachment, Comment, Tag)
from core.databases import session
from core.exceptions import (UploadErrorException, NotFoundErrorException,
                             CreateRowException, DeleteRowException)


class PostUsecase:
    def __init__(self):
        pass

    async def _is_liked(self, post_id: int, user_id: int) -> bool:
        pass


class GetPostUsecase(PostUsecase):
    async def execute(self, dto) -> PostEntity:
        pass


class FeedViewPostUsecase(PostUsecase):
    async def execute(self, dto: FeedViewPostDto) -> List[PostEntity]:
        query = session.query(Post).filter(Post.user_id != dto.user_id)\
            .order_by(Post.id.desc())
        if dto.prev:
            query = query.filter(Post.id > dto.prev)
        if dto.limit:
            query = query.limit(dto.limit)
        else:
            query = query.limit(self._get_default_limit())
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

    def _get_default_limit(self):
        return 24


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
    async def execute(self, dto) -> None:
        like = session.query(Post).filter().first()


class UnLikePostUsecase(PostUsecase):
    async def execute(self, dto) -> None:
        pass


class CreateCommentUsecase(PostUsecase):
    async def execute(self, dto: CreateCommentDto) -> Union[CommentEntity, NoReturn]:
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
