from dataclasses import dataclass


@dataclass
class GetUserDto:
    nickname: str = None


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
    user_id: int = None
    follow_user_id: int = None


@dataclass
class UnFollowUserDto:
    user_id: int = None
    follow_user_id: int = None
