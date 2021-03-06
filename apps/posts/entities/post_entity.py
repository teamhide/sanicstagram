from dataclasses import dataclass
from datetime import datetime
from typing import List, Union
from apps.users.entities import UserEntity


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
    comments: List['CommentEntity'] = None
    created_at: datetime = None
    updated_at: datetime = None


@dataclass
class PostEntity:
    id: int = None
    attachments: List = None
    caption: str = None
    user_id: int = None
    creator: int = None
    tags: Union[List[str], List] = None
    comments: Union[List[CommentEntity], List] = None
    is_liked: bool = None
    like_count: int = None
    created_at: datetime = None
    updated_at: datetime = None


@dataclass
class PostLikeEntity:
    id: int = None
    post_id: int = None
    user_id: int = None
    user: UserEntity = None
