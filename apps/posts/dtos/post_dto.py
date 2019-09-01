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
