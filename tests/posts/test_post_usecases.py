from unittest.mock import Mock

from tests.posts import post_entity, post_like_entity
from apps.posts.entities import PostEntity


def test_get_post_detail_usecase(post_entity, post_like_entity):
    repository = Mock()
    repository.get_post.return_value = post_entity
    repository.get_like.return_value = post_like_entity

    post_entity = repository.get_post(post_id=1)
    assert post_entity is not None

    if repository.get_like(post_id=1, user_id=1):
        is_liked = True
    else:
        is_liked = False

    post_entity.is_liked = is_liked
    assert post_entity.is_liked == True
    assert isinstance(post_entity, PostEntity) == True


def test_feed_view_post_usecase(post_entity):
    repository = Mock()
    repository.get_post_list.return_value = [post_entity]

    post_entities = repository.get_post_list()
    assert type(post_entities) == list
    for entity in post_entities:
        assert isinstance(entity, PostEntity)


def test_create_post_usecase(post_entity):
    repository = Mock()
    repository.save_post.return_value = post_entity

    post_entity = PostEntity(
        caption='caption',
        user_id=1,
    )


def test_like_post_usecase():
    repository = Mock()


def test_unlike_post_usecase():
    repository = Mock()


def test_create_comment_usecase():
    repository = Mock()


def test_delete_comment_usecase():
    repository = Mock()


def test_search_post_usecase():
    repository = Mock()


def test_get_post_liked_users_usecase():
    repository = Mock()


def test_search_tag_usecase():
    repository = Mock()


def test_delete_post_usecase():
    repository = Mock()


def test_update_post_usecase():
    repository = Mock()
