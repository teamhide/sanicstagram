import pytest

from tests import current_time
from apps.posts.entities import (PostEntity, CommentEntity, TagEntity, ImageEntity)
from apps.users.entities import UserEntity


@pytest.fixture
def image_entity(current_time):
    return ImageEntity(
        id=1,
        path='1.jpg',
        created_at=current_time,
        updated_at=current_time,
    )


@pytest.fixture
def tag_entity(current_time):
    return TagEntity(
        id=1,
        name='hash',
        created_at=current_time,
        updated_at=current_time,
    )


@pytest.fixture
def comment_entity(tag_entity, current_time):
    return CommentEntity(
        id=1,
        body='comment',
        creator=1,
        tags=[tag_entity],
        created_at=current_time,
        updated_at=current_time,
    )


@pytest.fixture
def user_entity(current_time):
    return UserEntity(
        id=1,
        nickname='hide',
        profile_image='hide.jpg',
        website='hides.kr',
        bio='bio',
        phone='010-1234-5678',
        gender='M',
        followers=[],
        followings=[],
        follower_count=10,
        following_count=20,
        created_at=current_time,
        updated_at=current_time,
    )


@pytest.fixture
def post_entity(user_entity, comment_entity, current_time):
    return PostEntity(
        id=1,
        attachments=[],
        caption='caption',
        user_id=1,
        creator=user_entity,
        tags=['hash', 'tags'],
        comments=[comment_entity],
        is_liked=True,
        like_count=20,
        created_at=current_time,
        updated_at=current_time,
    )
