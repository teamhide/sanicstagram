from typing import List
from uuid import uuid4

import sqlalchemy.exc

from apps.posts.dtos import CreatePostDto, FeedViewPostDto
from apps.posts.entities import PostEntity, CommentEntity
from apps.posts.models import Post, Attachment
from core.databases import session
from core.exceptions import UploadErrorException


class PostUsecase:
    def __init__(self):
        pass


class GetPostUsecase(PostUsecase):
    def execute(self, dto) -> PostEntity:
        pass


class FeedViewPostUsecase(PostUsecase):
    def execute(self, dto: FeedViewPostDto) -> List[PostEntity]:
        query = session.query(Post).filter(Post.creator != dto.user_id)\
            .order_by(Post.id.desc())
        if dto.prev:
            query = query.filter(Post.id < dto.prev)
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
                creator=post.creator,
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
    def execute(self, dto: CreatePostDto) -> PostEntity:
        post = Post(
            caption=dto.caption,
            creator=dto.user_id,
        )
        for attachment in dto.attachments:
            path = self._upload_attachment(attachment=attachment)
            post.attachments.append(Attachment(path=path))

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
            creator=post.creator,
            tags=post.tags,
            comments=post.comments,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )

    # TODO: S3에 업로드하는 코드 추가 필요
    def _upload_attachment(self, attachment) -> str:
        # 파일 객체의 실제 내용은 attachment.body에 담겨있음
        filename = uuid4().hex
        extension = attachment.name.split('.')[-1]
        return f'{filename}.{extension}'


class LikePostUsecase(PostUsecase):
    def execute(self, dto) -> None:
        pass


class UnLikePostUsecase(PostUsecase):
    def execute(self, dto) -> None:
        pass


class CreateCommentUsecase(PostUsecase):
    def execute(self, dto) -> CommentEntity:
        pass


class SearchPostUsecase(PostUsecase):
    def execute(self, dto) -> PostEntity:
        pass
