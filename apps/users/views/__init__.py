from sanic import Blueprint

from apps.users.views.v1 import (User, UserList, FollowUser, UnFollowUser,
                                 ExploreUsers, UserFollowers, UserFollowings)

bp = Blueprint('users', url_prefix='/api/v1')
bp.add_route(User.as_view(), '/users/<id:int>')
bp.add_route(UserList.as_view(), '/users')
bp.add_route(FollowUser.as_view(), '/<id:int>/follow')
bp.add_route(UnFollowUser.as_view(), '/<id:int>/unfollow')
bp.add_route(ExploreUsers.as_view(), '/explore')
bp.add_route(UserFollowers.as_view(), '/<id:int>/followers')
bp.add_route(UserFollowings.as_view(), '/<id:int>/followings')
