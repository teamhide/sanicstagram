from marshmallow import Schema, fields


class CreatePostSchema(Schema):
    attachments = fields.List(fields.Raw())
    caption = fields.Str(required=False)


class FeedViewPostSchema(Schema):
    prev = fields.Int(required=False)
    limit = fields.Int(required=True)
