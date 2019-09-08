import pytest
from unittest import mock


def test_get_post_detail_usecase():
    pass


def test_feed_view_post_usecase():
    pass


def test_create_post_usecase():
    pass


@mock.patch('apps.posts.repositories.post_repository.PostPSQLRepository')
def test_like_post_usecase(repository):
    post = repository.get_post(post_id=1)


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
