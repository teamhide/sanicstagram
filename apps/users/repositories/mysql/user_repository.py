import abc


class UserRepository:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def save_user(self):
        pass

    @abc.abstractmethod
    def get_user_list(self):
        pass

    @abc.abstractmethod
    def update_user(self):
        pass

    @abc.abstractmethod
    def follow_user(self, follower_id: int, following_id: int) -> None:
        pass

    @abc.abstractmethod
    def unfollow_user(self, follower_id: int, following_id: int) -> None:
        pass


class UserMySQLRepository(UserRepository):
    def save_user(self):
        pass

    def get_user_list(self):
        pass

    def update_user(self):
        pass

    def follow_user(self, follower_id: int, following_id: int) -> None:
        pass

    def unfollow_user(self, follower_id: int, following_id: int) -> None:
        pass
