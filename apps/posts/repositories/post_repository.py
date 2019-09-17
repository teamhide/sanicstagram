import abc
from typing import Optional, List, Union, NoReturn

import sqlalchemy.exc

from apps.posts.entities import PostEntity, CommentEntity
from apps.posts.enum import DefaultPaging
from apps.posts.models import Post, PostLike, Tag, Attachment, Comment
from apps.users.entities import UserEntity
from core.databases import session
from core.exceptions import CreateRowException, DeleteRowException


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
        tag: str = None,
        order: bool = None,
    ) -> List[PostEntity]:
        pass

    @abc.abstractmethod
    def get_like(self, post_id: int, user_id: int) -> Optional[PostLike]:
        pass

    @abc.abstractmethod
    def get_post_liked_users(
        self,
        post_id: int,
        prev: int = None,
        limit: int = None,
    ) -> List[UserEntity]:
        pass

    @abc.abstractmethod
    def update_post(
        self,
        post_id: int,
        caption: str = None,
        tags: List = None,
        reuse_attachment_id: int = None,
        attachments: List = None,
    ) -> Union[PostEntity, NoReturn]:
        pass

    @abc.abstractmethod
    def save_post(
        self,
        post_entity: PostEntity,
    ) -> Union[PostEntity, NoReturn]:
        pass

    @abc.abstractmethod
    def save_comment(
        self,
        post_id: int,
        body: str,
        user_id: int,
        parent_id: int = None,
    ) -> Union[CommentEntity, NoReturn]:
        pass

    @abc.abstractmethod
    def delete_post(self, post_id: int, user_id: int) -> Optional[NoReturn]:
        pass

    @abc.abstractmethod
    def delete_comment(
        self,
        comment_id: int,
        user_id: int,
    ) -> Optional[NoReturn]:
        pass

    @abc.abstractmethod
    def like_post(self, post_id: int, user_id: int) -> Optional[NoReturn]:
        pass

    @abc.abstractmethod
    def unlike_post(self, post_id: int, user_id: int) -> Optional[NoReturn]:
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
        tag: str = None,
        order: bool = None,
    ) -> List[PostEntity]:
        query = session.query(Post)

        if user_id:
            query = query.filter(Post.user_id != user_id)
        if tag:
            query = query.filter(Tag.name.in_([tag]))
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

    def get_like(self, post_id: int, user_id: int) -> Optional[PostLike]:
        return session.query(PostLike)\
            .filter(PostLike.post_id == post_id, Post.user_id == user_id)\
            .first()

    def get_post_liked_users(
        self,
        post_id: int,
        prev: int = None,
        limit: int = None,
    ) -> List[UserEntity]:
        query = session.query(PostLike).filter(PostLike.post_id == post_id)

        if prev:
            query = query.filter(PostLike.id > prev)
        if limit and limit < DefaultPaging.LIMIT.value:
            query = query.limit(limit)
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

    def update_post(
        self,
        post_id: int,
        caption: str = None,
        tags: List = None,
        reuse_attachment_id: int = None,
        attachments: List = None,
    ) -> Union[PostEntity, NoReturn]:
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
            raise CreateRowException

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

    def save_comment(
        self,
        post_id: int,
        body: str,
        user_id: int,
        parent_id: int = None,
    ) -> Union[CommentEntity, NoReturn]:
        post = session.query(Post).filter(Post.id == post_id).first()
        if parent_id:
            comment = Comment(body=body, user_id=user_id, parent_id=parent_id)
        else:
            comment = Comment(body=body, user_id=user_id)

        try:
            post.comments.append(comment)
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

    def delete_post(self, post_id: int, user_id: int) -> Optional[NoReturn]:
        post = session.query(Post).filter(
            Post.id == post_id,
            Post.user_id == user_id,
        ).first()

        try:
            session.delete(post)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            session.rollback()
            raise DeleteRowException

    def delete_comment(
        self,
        comment_id: int,
        user_id: int,
    ) -> Optional[NoReturn]:
        comment = session.query(Comment).filter(
            Comment.id == comment_id,
            Comment.user_id == user_id,
        ).first()

        try:
            session.delete(comment)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            session.rollback()
            raise DeleteRowException

    def like_post(self, post_id: int, user_id: int) -> Optional[NoReturn]:
        like = PostLike(
            post_id=post_id,
            user_id=user_id,
        )
        try:
            session.add(like)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            session.rollback()
            raise DeleteRowException

    def unlike_post(self, post_id: int, user_id: int) -> Optional[NoReturn]:
        like = session.query(PostLike).filter(
            post_id=post_id, user_id=user_id,
        ).first()
        try:
            session.delete(like)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            session.rollback()
            raise CreateRowException

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
