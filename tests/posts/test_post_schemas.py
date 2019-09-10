from apps.posts.schemas import (CreatePostRequestSchema,
                                FeedViewPostRequestSchema,
                                CreateCommentRequestSchema,
                                DeleteCommentRequestSchema,
                                GetPostLikedUsersRequestSchema,
                                SearchTagRequestSchema,
                                UpdatePostRequestSchema,
                                TagSchema,
                                CommentSchema,
                                AttachmentSchema,
                                PostSchema)


def test_create_post_request_schema():
    request = {'attachments': [], 'caption': 'caption'}
    validator = CreatePostRequestSchema().load(data=request)
    assert validator is not None
    assert type(validator['attachments']) == list
    assert validator['attachments'] == request['attachments']
    assert type(validator['caption']) == str
    assert validator['caption'] == request['caption']


def test_feed_view_post_request_schema():
    request = {'prev': 100, 'limit': 25}
    validator = FeedViewPostRequestSchema().load(data=request)
    assert validator is not None
    assert type(validator['prev']) == int
    assert validator['prev'] == request['prev']
    assert type(validator['limit']) == int
    assert validator['limit'] == request['limit']


def test_create_comment_request_schema():
    request = {'body': 'comment'}
    validator = CreateCommentRequestSchema().load(data=request)
    assert validator is not None
    assert type(validator['body']) == str
    assert validator['body'] == request['body']


def test_delete_comment_request_schema():
    request = {'post_id': 1, 'comment_id': 1}
    validator = DeleteCommentRequestSchema().load(data=request)
    assert validator is not None
    assert type(validator['post_id']) == int
    assert validator['post_id'] == request['post_id']
    assert type(validator['comment_id']) == int
    assert validator['comment_id'] == request['comment_id']


def test_get_post_liked_users_request_schema():
    request = {'prev': 100, 'limit': 25}
    validator = GetPostLikedUsersRequestSchema().load(data=request)
    assert validator is not None
    assert type(validator['prev']) == int
    assert validator['prev'] == request['prev']
    assert type(validator['limit']) == int
    assert validator['limit'] == request['limit']


def test_search_tag_request_schema():
    request = {'prev': 100, 'limit': 25, 'tag': 'hashtag'}
    validator = SearchTagRequestSchema().load(data=request)
    assert validator is not None
    assert type(validator['prev']) == int
    assert validator['prev'] == request['prev']
    assert type(validator['limit']) == int
    assert validator['limit'] == request['limit']
    assert type(validator['tag']) == str
    assert validator['tag'] == request['tag']


def test_update_post_request_schema():
    request = {
        'caption': 'caption',
        'reuse_attachment_id': 1,
        'attachments': [],
    }
    validator = UpdatePostRequestSchema().load(data=request)
    assert validator is not None
    assert type(validator['caption']) == str
    assert validator['caption'] == request['caption']
    assert type(validator['reuse_attachment_id']) == int
    assert validator['reuse_attachment_id'] == request['reuse_attachment_id']
    assert type(validator['attachments']) == list
    assert validator['attachments'] == request['attachments']


def test_tag_schema():
    request = {'name': 'name'}
    validator = TagSchema().load(data=request)
    assert validator is not None
    assert type(validator['name']) == str
    assert validator['name'] == request['name']


def test_comment_schema():
    pass


def test_attachment_schema():
    pass


def test_post_schema():
    pass


def test_create_psot_response_schema():
    pass


def test_feed_view_post_response_schema():
    pass


def test_create_comment_response_schema():
    pass


def test_post_detail_response_schema():
    pass
