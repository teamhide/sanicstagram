from typing import List, Optional

import sqlalchemy.exc

from apps.users.dtos import (FollowUserDto, UnFollowUserDto)
from apps.users.entities import UserEntity
from apps.users.models import Follow, User
from core.databases import session


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


class ExploreUsersUsecase(UserUsecase):
    def execute(self) -> Optional[List[UserEntity]]:
        users = session.query(User).order_by(User.id.desc()).all()[:5]
        if not users:
            return

        user_entities = [
            UserEntity(
                id=user.id,
                profile_image=user.profile_image,
                name=user.name,
            )
            for user in users
        ]
        return user_entities


class LoginUsecase(UserUsecase):
    def execute(self, dto):
        pass

    def _default_login(self):
        pass

    def _social_login(self):
        pass
