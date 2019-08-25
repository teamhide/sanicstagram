from apps.users.repositories.mysql import UserMySQLRepository


class UserUsecase:
    def __init__(self):
        self.repository = UserMySQLRepository()


class RegisterUserUsecase(UserUsecase):
    pass


class GetUserListUsecase(UserUsecase):
    pass


class UpdateUserUsecase(UserUsecase):
    pass


class FollowUserUsecase(UserUsecase):
    pass


class UnFollowUserUsecase(UserUsecase):
    pass
