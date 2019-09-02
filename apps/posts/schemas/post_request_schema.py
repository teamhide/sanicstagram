from marshmallow import Schema, fields


class CreatePostRequestSchema(Schema):
    attachments = fields.List(fields.Raw())
    caption = fields.Str(required=False)


class FeedViewPostRequestSchema(Schema):
    prev = fields.Int(required=False)
    limit = fields.Int(required=True)


class CreateCommentRequestSchema(Schema):
    body = fields.Str(required=True)
