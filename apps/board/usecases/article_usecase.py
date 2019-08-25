from apps.board.repositories import ArticleMySQLRepository


class ArticleUsecase:
    def __init__(self):
        self.repository = ArticleMySQLRepository()


class CreateArticleUsecase(ArticleUsecase):
    def execute(self):
        pass


class GetArticleListUsecase(ArticleUsecase):
    def execute(self):
        pass
