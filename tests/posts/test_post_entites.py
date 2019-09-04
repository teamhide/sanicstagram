from datetime import datetime

from apps.posts.entities import (PostEntity, ImageEntity, CommentEntity,
                                 TagEntity)


def get_current_time() -> datetime:
    return datetime.utcnow().replace(microsecond=0)


def test_post_entity():
    current_time = get_current_time()

    entity = PostEntity(
        id=1,
        attachments=[],
        caption='post',
        creator=1,
        tags=[],
        comments=[],
        is_liked=True,
        like_count=1,
        created_at=current_time,
        updated_at=current_time,
    )
    assert entity.id == 1
    assert entity.attachments == []
    assert entity.caption == 'post'
    assert entity.creator == 1
    assert entity.tags == []
    assert entity.comments == []
    assert entity.is_liked == True
    assert entity.like_count == 1
    assert entity.created_at == current_time
    assert entity.updated_at == current_time


def test_image_entity():
    current_time = get_current_time()

    entity = ImageEntity(
        id=1,
        path='1.jpg',
        created_at=current_time,
        updated_at=current_time,
    )
    assert entity.id == 1
    assert entity.path == '1.jpg'
    assert entity.created_at == current_time
    assert entity.updated_at == current_time


def test_comment_entity():
    current_time = get_current_time()

    entity = CommentEntity(
        id=1,
        body='body',
        creator=1,
        tags=[],
        created_at=current_time,
        updated_at=current_time,
    )
    assert entity.id == 1
    assert entity.body == 'body'
    assert entity.creator == 1
    assert entity.tags == []
    assert entity.created_at == current_time
    assert entity.updated_at == current_time


def test_tag_entity():
    current_time = get_current_time()

    entity = TagEntity(
        id=1,
        name='hashtag',
        created_at=current_time,
        updated_at=current_time,
    )
    assert entity.id == 1
    assert entity.name == 'hashtag'
    assert entity.created_at == current_time
    assert entity.updated_at == current_time
