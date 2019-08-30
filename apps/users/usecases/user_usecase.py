from typing import List, Optional

import sqlalchemy.exc

from apps.users.dtos import (FollowUserDto, UnFollowUserDto, GetUserDto)
from apps.users.entities import UserEntity
from apps.users.models import User
from core.databases import session
from core.exceptions import NotFoundErrorException


class UserUsecase:
    def __init__(self):
        pass

    def _is_followed(self, user_id: int, target_user_id: int) -> bool:
        user = session.query(User).filter(User.id == user_id).first() \
            .followings.filter(User.id == target_user_id).first()
        return user is not None


class GetUserUsecase(UserUsecase):
    def execute(self, dto: GetUserDto) -> UserEntity:
        user = session.query(User)\
            .filter(User.nickname == dto.nickname).first()
        if not user:
            raise NotFoundErrorException

        return UserEntity(
            nickname=user.nickname,
            profile_image=user.profile_image,
            bio=user.bio,
            website=user.website,
            followers=user.followers,
            followings=user.followings,
        )


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
                target_user_id=dto.follow_user_id,
        ):
            return

        user = session.query(User).filter(User.id == dto.user_id).first()
        try:
            target_user = session.query(User)\
                .filter(User.id == dto.follow_user_id).first()
            user.followings.append(target_user)
            session.add(user)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            session.rollback()


class UnFollowUserUsecase(UserUsecase):
    def execute(self, dto: UnFollowUserDto) -> None:
        if not self._is_followed(
                user_id=dto.user_id,
                target_user_id=dto.follow_user_id,
        ):
            return

        user = session.query(User).filter(User.id == dto.user_id).first()
        try:
            target_user = session.query(User)\
                .filter(User.id == dto.follow_user_id).first()
            user.followings.remove(target_user)
            session.add(user)
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
                nickname=user.nickname,
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


class GetUserFollowersUsecase(UserUsecase):
    def execute(self, user_id: int) -> List[UserEntity]:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundErrorException
        return [
            UserEntity(
                id=follower.id,
                nickname=follower.nickname,
                profile_image=follower.profile_image,
                website=follower.website,
                bio=follower.bio,
                phone=follower.phone,
                gender=follower.gender,
            )
            for follower in user.followers
        ]


class GetUserFollowingsUsecase(UserUsecase):
    def execute(self, user_id: int) -> List[UserEntity]:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundErrorException
        return [
            UserEntity(
                id=followings.id,
                nickname=followings.nickname,
                profile_image=followings.profile_image,
                website=followings.website,
                bio=followings.bio,
                phone=followings.phone,
                gender=followings.gender,
            )
            for followings in user.followings
        ]


class SearchUserUsecase(UserUsecase):
    def execute(self, nickname: str) -> List[UserEntity]:
        users = session.query(User)\
            .filter(User.nickname.like(nickname)).all()
        return [
            UserEntity(
                id=user.id,
                nickname=user.nickname,
                profile_image=user.profile_image,
                website=user.website,
                bio=user.bio,
                phone=user.phone,
                gender=user.gender,
            )
            for user in users
        ]
