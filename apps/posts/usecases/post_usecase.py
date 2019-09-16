import re
from typing import List, Union, NoReturn, Optional
from uuid import uuid4

from apps.posts.dtos import (CreatePostDto, FeedViewPostDto, CreateCommentDto,
                             DeleteCommentDto, LikePostDto,
                             GetPostLikedUsersDto, SearchTagDto, DeletePostDto,
                             GetPostDto, UpdatePostDto)
from apps.posts.entities import PostEntity, CommentEntity
from apps.posts.repositories import PostPSQLRepository
from apps.users.entities import UserEntity
from core.exceptions import (NotFoundErrorException,
                             AlreadyDoneException, PermissionException)


class PostUsecase:
    def __init__(self):
        self.repository = PostPSQLRepository()


class GetPostDetailUsecase(PostUsecase):
    async def execute(self, dto: GetPostDto) -> Union[PostEntity, NoReturn]:
        post_entity = self.repository.get_post(post_id=dto.post_id)
        if not post_entity:
            raise NotFoundErrorException

        post_entity.is_liked = True if self.repository.get_like(post_id=dto.post_id, user_id=dto.user_id) else False  # noqa
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
    async def execute(self, dto: LikePostDto) -> Optional[NoReturn]:
        if self.repository.get_like(post_id=dto.post_id, user_id=dto.user_id):
            raise AlreadyDoneException

        self.repository.like_post(post_id=dto.post_id, user_id=dto.user_id)


class UnLikePostUsecase(PostUsecase):
    async def execute(self, dto) -> Optional[NoReturn]:
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
            parent_id=dto.parent_id,
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
        liked_users = self.repository.get_post_liked_users(
            post_id=dto.post_id,
            prev=dto.prev,
            limit=dto.limit,
        )
        return liked_users


class SearchTagUsecase(PostUsecase):
    async def execute(self, dto: SearchTagDto) -> List[PostEntity]:
        posts = self.repository.get_post_list(
            user_id=dto.user_id,
            tag=dto.tag,
            prev=dto.prev,
            limit=dto.limit,
            order=True,
        )
        return posts


class DeletePostUsecase(PostUsecase):
    async def execute(self, dto: DeletePostDto) -> Optional[NoReturn]:
        post = self.repository.get_post(post_id=dto.post_id)
        if post.user_id != dto.user_id:
            raise PermissionException

        self.repository.delete_post(post_id=dto.post_id, user_id=dto.user_id)


class UpdatePostUsecase(PostUsecase):
    async def execute(self, dto: UpdatePostDto) -> Optional[NoReturn]:
        post = self.repository.get_post(post_id=dto.post_id)
        if post.user_id != dto.user_id:
            raise PermissionException

        await self._process_update_post(dto=dto)

        return self.repository.update_post(
            post_id=dto.post_id,
            caption=dto.caption,
        )

    async def _process_update_post(
        self,
        dto: UpdatePostDto,
    ) -> None:
        if dto.reuse_attachment_id:
            pass
        if dto.attachments:
            pass
        if dto.caption:
            pass
