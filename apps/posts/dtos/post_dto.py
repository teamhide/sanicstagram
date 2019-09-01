from dataclasses import dataclass
from typing import List


@dataclass
class CreatePostDto:
    user_id: int = None
    attachments: List = None
    caption: str = None
