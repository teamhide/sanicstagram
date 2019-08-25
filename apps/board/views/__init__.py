from sanic import Blueprint

from apps.board.views.v1 import Article, ArticleList

bp = Blueprint('article', url_prefix='/api/v1')
bp.add_route(Article.as_view(), '/article/<id:int>')
bp.add_route(ArticleList.as_view(), '/article')
