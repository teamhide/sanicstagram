from sanic import Blueprint

from apps.users.views.v1 import (User, UserList, FollowUser, UnFollowUser,
                                 ExploreUsers, UserFollowers, UserFollowings,
                                 Login, UserProfile)

bp = Blueprint('users', url_prefix='/api/v1')
bp.add_route(User.as_view(), '/users/<user_id:int>')
bp.add_route(UserList.as_view(), '/users')
bp.add_route(UserProfile.as_view(), '/users/<name:string>')
bp.add_route(FollowUser.as_view(), '/<user_id:int>/follow')
bp.add_route(UnFollowUser.as_view(), '/<user_id:int>/unfollow')
bp.add_route(ExploreUsers.as_view(), '/explore')
bp.add_route(UserFollowers.as_view(), '/<user_id:int>/followers')
bp.add_route(UserFollowings.as_view(), '/<user_id:int>/followings')
bp.add_route(Login.as_view(), '/login')
