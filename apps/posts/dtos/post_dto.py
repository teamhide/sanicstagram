from dataclasses import dataclass
from typing import List


@dataclass
class CreatePostDto:
    user_id: int = None
    attachments: List = None
    caption: str = None


@dataclass
class FeedViewPostDto:
    user_id: int = None
    prev: int = None
    limit: int = None


@dataclass
class CreateCommentDto:
    user_id: int = None
    post_id: int = None
    body: str = None


@dataclass
class DeleteCommentDto:
    user_id: int = None
    post_id: int = None
    comment_id: int = None


@dataclass
class LikePostDto:
    user_id: int = None
    post_id: int = None


@dataclass
class UnLikePostDto:
    user_id: int = None
    post_id: int = None


@dataclass
class GetPostLikedUsersDto:
    user_id: int = None
    post_id: int = None
    prev: int = None
    limit: int = None


@dataclass
class SearchTagDto:
    user_id: int = None
    prev: int = None
    limit: int = None
    tag: str = None


@dataclass
class DeletePostDto:
    user_id: int = None
    post_id: int = None


@dataclass
class GetPostDto:
    user_id: int = None
    post_id: int = None


@dataclass
class UpdatePostDto:
    user_id: int = None
    post_id: int = None
    caption: str = None
    reuse_attachment_id: int = None
    attachments: List = None
