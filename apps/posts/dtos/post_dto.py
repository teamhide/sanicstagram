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
