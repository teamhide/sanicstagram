import abc


class ArticleRepository:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_article(self):
        pass

    @abc.abstractmethod
    def get_article_list(self):
        pass


class ArticleMySQLRepository(ArticleRepository):
    def create_article(self):
        pass

    def get_article_list(self):
        pass
