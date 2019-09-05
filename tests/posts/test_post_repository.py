import pytest

from apps.posts.models import (Post, Attachment, Comment, Tag, PostLike)
from apps.users.models import User
from tests import current_time


@pytest.fixture
def user_model(current_time):
    return User(
        id=1,
        email='john@hides.kr',
        nickname='hide',
        profile_image='hide.png',
        website='http://hides.kr',
        bio='bio',
        phone='010-1234-5678',
        gender='M',
        followers=[],
        followings=[],
        created_at=current_time,
        updated_at=current_time,
    )


@pytest.fixture
def attachment_model(current_time):
    return Attachment(
        id=1,
        path='test.jpg',
        created_at=current_time,
        updated_at=current_time,
    )


@pytest.fixture
def tag_model(current_time):
    return Tag(
        id=1,
        name='hashtag',
        created_at=current_time,
        updated_at=current_time,
    )


@pytest.fixture
def post_like_model(current_time, user_model):
    return PostLike(
        id=1,
        post_id=1,
        user_id=1,
        user=user_model,
    )


@pytest.fixture
def comment_model(user_model, tag_model):
    return Comment(
        id=1,
        body='comment',
        user_id=1,
        creator=user_model,
        tags=[tag_model],
    )


@pytest.fixture
def post_model(
    attachment_model,
    user_model,
    comment_model,
    tag_model,
    post_like_model,
):
    return Post(
        id=1,
        attachments=attachment_model,
        caption='post caption',
        user_id=1,
        creator=user_model,
        comments=comment_model,
        tags=tag_model,
        likes=post_like_model,
    )


def test_get_post(post_model):
    pass
