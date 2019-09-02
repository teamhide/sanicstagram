from marshmallow import Schema, fields


class TagSchema(Schema):
    name = fields.Str()


class CommentSchema(Schema):
    id = fields.Int()
    body = fields.Str()
    creator = fields.Str()
    tags = fields.Nested(TagSchema)


class AttachmentSchema(Schema):
    id = fields.Int()
    path = fields.Str()


class PostSchema(Schema):
    id = fields.Int()
    caption = fields.Str()
    creator = fields.Str()


class CreatePostResponseSchema(PostSchema):
    attachments = fields.List(fields.Nested(AttachmentSchema))
    comments = fields.List(fields.Nested(CommentSchema))
    tags = fields.List(fields.Nested(TagSchema))


class FeedViewPostResponseSchema(PostSchema):
    attachments = fields.List(fields.Nested(AttachmentSchema))
    comments = fields.List(fields.Nested(CommentSchema))
    tags = fields.List(fields.Nested(TagSchema))
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class CreateCommentResponseSchema(PostSchema):
    id = fields.Int()
    body = fields.Str()
    creator = fields.Str()
