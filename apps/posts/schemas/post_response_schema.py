from marshmallow import Schema, fields


class TagSchema(Schema):
    name = fields.Str()


class CommentSchema(Schema):
    id = fields.Int()
    body = fields.Str()
    creator = fields.Int()
    tags = fields.Nested(TagSchema)


class AttachmentSchema(Schema):
    id = fields.Int()
    path = fields.Str()


class CreatePostResponseSchema(Schema):
    id = fields.Int()
    attachments = fields.List(fields.Nested(AttachmentSchema))
    caption = fields.Str()
    creator = fields.Int()
    comments = fields.List(fields.Nested(CommentSchema))
    tags = fields.List(fields.Nested(TagSchema))


class FeedViewPostResponseSchema(Schema):
    id = fields.Int()
    attachments = fields.List(fields.Nested(AttachmentSchema))
    caption = fields.Str()
    creator = fields.Int()
    comments = fields.List(fields.Nested(CommentSchema))
    tags = fields.List(fields.Nested(TagSchema))
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
