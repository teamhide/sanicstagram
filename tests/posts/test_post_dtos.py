from apps.posts.dtos import (CreatePostDto, FeedViewPostDto, CreateCommentDto,
                             DeleteCommentDto, LikePostDto, UnLikePostDto,
                             GetPostLikedUsersDto, SearchTagDto, DeletePostDto,
                             GetPostDto, UpdatePostDto)


def test_create_post_dto():
    dto = CreatePostDto(
        user_id=1,
        attachments=[],
        caption='first caption'
    )
    assert dto.user_id == 1
    assert dto.attachments == []
    assert dto.caption == 'first caption'


def test_feed_view_post_dto():
    dto = FeedViewPostDto(
        user_id=1,
        prev=1,
        limit=1
    )
    assert dto.user_id == 1
    assert dto.prev == 1
    assert dto.limit == 1


def test_create_comment_dto():
    dto = CreateCommentDto(
        user_id=1,
        post_id=2,
        body='body'
    )
    assert dto.user_id == 1
    assert dto.post_id == 2
    assert dto.body == 'body'


def test_delete_comment_dto():
    dto = DeleteCommentDto(
        user_id=1,
        post_id=2,
        comment_id=3,
    )
    assert dto.user_id == 1
    assert dto.post_id == 2
    assert dto.comment_id == 3


def test_like_post_dto():
    dto = LikePostDto(
        user_id=1,
        post_id=2,
    )
    assert dto.user_id == 1
    assert dto.post_id == 2


def test_unlike_post_dto():
    dto = UnLikePostDto(
        user_id=1,
        post_id=2,
    )
    assert dto.user_id == 1
    assert dto.post_id == 2


def test_get_post_liked_user_dto():
    dto = GetPostLikedUsersDto(
        user_id=1,
        post_id=2,
        prev=1,
        limit=2,
    )
    assert dto.user_id == 1
    assert dto.post_id == 2
    assert dto.prev == 1
    assert dto.limit == 2


def test_search_tag_dto():
    dto = SearchTagDto(
        user_id=1,
        prev=2,
        limit=3,
        tag='hashtag'
    )
    assert dto.user_id == 1
    assert dto.prev == 2
    assert dto.limit == 3
    assert dto.tag == 'hashtag'


def test_delete_post_dto():
    dto = DeletePostDto(
        user_id=1,
        post_id=2,
    )
    assert dto.user_id == 1
    assert dto.post_id == 2


def test_get_post_dto():
    dto = GetPostDto(
        user_id=1,
        post_id=2,
    )
    assert dto.user_id == 1


def test_update_post_dto():
    dto = UpdatePostDto(
        user_id=1,
        post_id=2,
        caption='caption',
        reuse_attachment_id=1,
        attachments=[]
    )
    assert dto.user_id == 1
    assert dto.post_id == 2
    assert dto.caption == 'caption'
    assert dto.reuse_attachment_id == 1
    assert dto.attachments == []
