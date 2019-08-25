from dataclasses import dataclass


@dataclass
class RegisterUserDto:
    pass


@dataclass
class GetUserListDto:
    pass


@dataclass
class UpdateUserDto:
    pass


@dataclass
class FollowUserDto:
    follower_id: int = None
    following_id: str = None


@dataclass
class UnFollowUserDto:
    follower_id: int = None
    following_id: str = None
