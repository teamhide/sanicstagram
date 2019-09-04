from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class PostEntity:
    id: int = None
    attachments: List = None
    caption: str = None
    creator: int = None
    tags: List = None
    comments: List = None
    is_liked: bool = None
    like_count: int = None
    created_at: datetime = None
    updated_at: datetime = None


@dataclass
class ImageEntity:
    id: int = None
    path: str = None
    created_at: datetime = None
    updated_at: datetime = None


@dataclass
class CommentEntity:
    id: int = None
    body: str = None
    creator: int = None
    tags: List = None
    created_at: datetime = None
    updated_at: datetime = None


@dataclass
class TagEntity:
    id: int = None
    name: int = None
    created_at: datetime = None
    updated_at: datetime = None
