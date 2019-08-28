from apps.users.dtos import (FollowUserDto, UnFollowUserDto)
from core.databases import session
from apps.users.models import User, Follow
import sqlalchemy.exc


class UserUsecase:
    def __init__(self):
        pass

    def _is_followed(self, user_id: int, follow_user_id: int) -> bool:
        is_exist = session.query(Follow)\
            .filter(
            Follow.follower_id == user_id,
            Follow.following_id == follow_user_id,
        ).first()
        return is_exist is not None


class RegisterUserUsecase(UserUsecase):
    def execute(self, dto):
        pass


class GetUserListUsecase(UserUsecase):
    def execute(self, dto):
        pass


class UpdateUserUsecase(UserUsecase):
    def execute(self, dto):
        pass


class FollowUserUsecase(UserUsecase):
    def execute(self, dto: FollowUserDto) -> None:
        if self._is_followed(
                user_id=dto.user_id,
                follow_user_id=dto.follow_user_id,
        ):
            return

        try:
            relationship = Follow(
                follower_id=dto.user_id,
                following_id=dto.follow_user_id,
            )
            session.add(relationship)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            session.rollback()


class UnFollowUserUsecase(UserUsecase):
    def execute(self, dto: UnFollowUserDto) -> None:
        if not self._is_followed(
                user_id=dto.user_id,
                follow_user_id=dto.follow_user_id,
        ):
            return

        try:
            relationship = Follow(
                follower_id=dto.user_id,
                following_id=dto.follow_user_id,
            )
            session.delete(relationship)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            session.rollback()


class LoginUsecase(UserUsecase):
    def execute(self, dto):
        pass

    def _default_login(self):
        pass

    def _social_login(self):
        pass
