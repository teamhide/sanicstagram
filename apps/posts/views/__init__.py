from sanic import Blueprint

from apps.posts.views.v1 import (Post, PostList, LikePost, UnLikePost, Comment,
                                 SearchPost, GetPostLikedUsers)

bp = Blueprint('posts', url_prefix='/api/v1')
bp.add_route(Post.as_view(), '/posts/<post_id:int>')
bp.add_route(PostList.as_view(), '/posts')
bp.add_route(LikePost.as_view(), '/posts/<post_id:int>/like')
bp.add_route(UnLikePost.as_view(), '/posts/<post_id:int>/unlike')
bp.add_route(Comment.as_view(), '/posts/<post_id:int>/comment')
bp.add_route(Comment.as_view(), '/posts/<post_id:int>/comment/<comment_id:int>')  # noqa
bp.add_route(SearchPost.as_view(), '/posts/search')
bp.add_route(GetPostLikedUsers.as_view(), '/posts/<post_id:int>/liked_user')
