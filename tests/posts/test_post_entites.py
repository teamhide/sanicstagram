from apps.posts.entities import (PostEntity, ImageEntity, CommentEntity, TagEntity)
from datetime import datetime


def test_post_entity():
    entity = PostEntity(
        id=1,
        attachments=[],
        caption='post',
        creator=1,
        tags=[],
        comments=[],
        is_liked=True,
        like_count=1,
        created_at=datetime.utcnow().replace(microsecond=0),
        updated_at=datetime.utcnow().replace(microsecond=0),
    )
    assert entity.id == 1
    assert entity.attachments == []
    assert entity.caption == 'post'
    assert entity.creator == 1
    assert entity.tags == []
    assert entity.comments == []
    assert entity.is_liked == True
    assert entity.like_count == 1
    assert entity.created_at == datetime.utcnow().replace(microsecond=0)
    assert entity.updated_at == datetime.utcnow().replace(microsecond=0)


def test_image_entity():
    entity = ImageEntity()


def test_comment_entity():
    entity = CommentEntity()


def test_tag_entity():
    entity = TagEntity()
