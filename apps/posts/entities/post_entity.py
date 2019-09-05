from dataclasses import dataclass
from datetime import datetime
from typing import List, Union


@dataclass
class ImageEntity:
    id: int = None
    path: str = None
    created_at: datetime = None
    updated_at: datetime = None


@dataclass
class TagEntity:
    id: int = None
    name: str = None
    created_at: datetime = None
    updated_at: datetime = None


@dataclass
class CommentEntity:
    id: int = None
    body: str = None
    creator: int = None
    tags: List[TagEntity] = None
    created_at: datetime = None
    updated_at: datetime = None


@dataclass
class PostEntity:
    id: int = None
    attachments: List = None
    caption: str = None
    creator: int = None
    tags: Union[List[str], List] = None
    comments: Union[List[CommentEntity], List] = None
    is_liked: bool = None
    like_count: int = None
    created_at: datetime = None
    updated_at: datetime = None
