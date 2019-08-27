from apps.users.dtos import (FollowUserDto, UnFollowUserDto)
from apps.users.repositories.mysql import UserMySQLRepository


class UserUsecase:
    def __init__(self):
        self.repository = UserMySQLRepository()


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
    def execute(self, dto: FollowUserDto):
        pass


class UnFollowUserUsecase(UserUsecase):
    def execute(self, dto: UnFollowUserDto):
        pass


class LoginUsecase(UserUsecase):
    def execute(self, dto):
        pass

    def _default_login(self):
        pass

    def _social_login(self):
        pass
