from dataclasses import dataclass
from typing import List


@dataclass
class UserEntity:
    id: int = None
    nickname: str = None
    profile_image: str = None
    website: str = None
    bio: str = None
    phone: str = None
    gender: str = None
    followers: List = None
    followings: List = None
    follower_count: int = None
    following_count: int = None
