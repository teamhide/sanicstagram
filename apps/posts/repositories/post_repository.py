import abc
from typing import Optional, List, Union, NoReturn

import sqlalchemy.exc

from apps.posts.entities import PostEntity
from apps.posts.enum import DefaultPaging
from apps.posts.models import (Post, PostLike, Tag, Attachment)
from core.databases import session


class PostRepository:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_post(
        self,
        post_id: int = None,
        user_id: int = None,
    ) -> Optional[PostEntity]:
        pass

    @abc.abstractmethod
    def get_post_list(
        self,
        user_id: int = None,
        prev: int = None,
        limit: int = None,
        order: bool = None,
    ) -> List[PostEntity]:
        pass

    @abc.abstractmethod
    def get_likes(self, post_id: int, user_id: int) -> Optional[PostLike]:
        pass

    @abc.abstractmethod
    def update_post(self):
        pass

    @abc.abstractmethod
    def save_post(
        self,
        post_entity: PostEntity,
    ) -> Union[PostEntity, NoReturn]:
        pass

    @abc.abstractmethod
    def delete_post(self):
        pass


class PostPSQLRepository(PostRepository):
    def get_post(
        self,
        post_id: int = None,
        user_id: int = None,
    ) -> Optional[PostEntity]:
        query = session.query(Post)

        if post_id:
            query = query.filter(Post.id == post_id)
        if user_id:
            query = query.filter(Post.user_id == user_id)

        post = query.first()
        if not post:
            return

        return PostEntity(
            id=post.id,
            attachments=post.attachments,
            caption=post.caption,
            creator=post.creator.nickname,
            tags=post.tags,
            comments=post.comments,
            like_count=post.likes_count,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )

    def get_post_list(
        self,
        user_id: int = None,
        prev: int = None,
        limit: int = None,
        order: bool = None,
    ) -> List[PostEntity]:
        query = session.query(Post)

        if user_id:
            query = query.filter(Post.user_id != user_id)
        if order is True:
            query = query.order_by(Post.id.desc())
        if prev:
            query = query.filter(Post.id > prev)
        if limit:
            query = query.limit(limit)
        else:
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

    def get_likes(self, post_id: int, user_id: int) -> Optional[PostLike]:
        return session.query(PostLike)\
            .filter(PostLike.post_id == post_id, Post.user_id == user_id)\
            .first()

    def update_post(self):
        pass

    def save_post(
        self,
        post_entity: PostEntity,
    ) -> Union[PostEntity, NoReturn]:
        post = Post(
            caption=post_entity.caption,
            user_id=post_entity.user_id,
        )

        if post_entity.attachments:
            post.attachments = self._process_attachments(
                attachments=post_entity.attachments,
            )

        if post_entity.tags:
            post.tags = self._process_tags(tags=post_entity.tags)

        try:
            session.add(post)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            session.rollback()
            raise

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

    def delete_post(self):
        pass

    def _convert_tags_to_list(self, tags: List) -> List:
        return [
            tag[0]
            for tag in tags
        ]

    def _process_attachments(self, attachments: List) -> List[Attachment]:
        return [
            Attachment(path=attachment)
            for attachment in attachments
        ]

    def _process_tags(self, tags: List) -> List[Tag]:
        result = []
        saved_tags = self._convert_tags_to_list(
            tags=session.query(Tag.name).filter(
                Tag.name.in_(tags)).all(),
            )

        for tag in tags:
            if tag in saved_tags:
                result.append(
                    session.query(Tag).filter(Tag.name == tag).first(),
                )
            else:
                result.append(Tag(name=tag))

        return result
