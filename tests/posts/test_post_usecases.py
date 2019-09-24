from unittest.mock import patch

from apps.posts.usecases import GetPostDetailUsecase
from apps.posts.dtos import GetPostDto


@patch('apps.posts.repositories.PostPSQLRepository.get_post')
@patch('apps.posts.repositories.PostPSQLRepository.get_like')
async def test_get_post_detail_usecase(get_like, get_post):
    post_entity = await GetPostDetailUsecase().execute(
        dto=GetPostDto(post_id=1, user_id=1),
    )


def test_feed_view_post_usecase(post_entity):
    pass

def test_create_post_usecase(post_entity):
    pass


def test_like_post_usecase():
    pass


def test_unlike_post_usecase():
    pass


def test_create_comment_usecase():
    pass


def test_delete_comment_usecase():
    pass


def test_search_post_usecase():
    pass


def test_get_post_liked_users_usecase():
    pass


def test_search_tag_usecase():
    pass


def test_delete_post_usecase():
    pass


def test_update_post_usecase():
    pass
