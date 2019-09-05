import abc


class PostRepository:
    __metaclass__ = abc.ABCMeta

    def __new__(cls, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_post(self, post_id: int):
        pass

    @abc.abstractmethod
    def get_post_list(self):
        pass

    @abc.abstractmethod
    def update_post(self):
        pass

    @abc.abstractmethod
    def save_post(self):
        pass

    @abc.abstractmethod
    def delete_post(self):
        pass
