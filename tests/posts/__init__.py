from datetime import datetime

import pytest

from apps.posts.entities import (PostEntity, CommentEntity, TagEntity,
                                 ImageEntity, PostLikeEntity)
from apps.users.entities import UserEntity


@pytest.fixture
def image_entity():
    return ImageEntity(
        id=1,
        path='1.jpg',
        created_at=datetime.utcnow().replace(microsecond=0),
        updated_at=datetime.utcnow().replace(microsecond=0),
    )


@pytest.fixture
def tag_entity():
    return TagEntity(
        id=1,
        name='hash',
        created_at=datetime.utcnow().replace(microsecond=0),
        updated_at=datetime.utcnow().replace(microsecond=0),
    )


@pytest.fixture
def comment_entity():
    return CommentEntity(
        id=1,
        body='comment',
        creator=1,
        tags=[tag_entity],
        created_at=datetime.utcnow().replace(microsecond=0),
        updated_at=datetime.utcnow().replace(microsecond=0),
    )


@pytest.fixture
def user_entity():
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
        created_at=datetime.utcnow().replace(microsecond=0),
        updated_at=datetime.utcnow().replace(microsecond=0),
    )


@pytest.fixture
def post_entity():
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
        created_at=datetime.utcnow().replace(microsecond=0),
        updated_at=datetime.utcnow().replace(microsecond=0),
    )


@pytest.fixture
def post_like_entity():
    return PostLikeEntity(
        id=1,
        post_id=1,
        user_id=2,
        user=user_entity,
    )
