from marshmallow import Schema, fields


class CreatePostRequestSchema(Schema):
    attachments = fields.List(fields.Raw())
    caption = fields.String(required=False)


class FeedViewPostRequestSchema(Schema):
    prev = fields.Integer(required=False)
    limit = fields.Integer(required=True)


class CreateCommentRequestSchema(Schema):
    parent_id = fields.Integer(required=False)
    body = fields.String(required=True)


class DeleteCommentRequestSchema(Schema):
    post_id = fields.Integer(required=True)
    comment_id = fields.Integer(required=True)


class GetPostLikedUsersRequestSchema(Schema):
    prev = fields.Integer(required=False)
    limit = fields.Integer(required=False)


class SearchTagRequestSchema(Schema):
    prev = fields.Integer(required=False)
    limit = fields.Integer(required=False)
    tag = fields.String(required=True)


class UpdatePostRequestSchema(Schema):
    caption = fields.String(required=False)
    reuse_attachment_id = fields.Integer(required=False)
    attachments = fields.List(fields.Raw())
