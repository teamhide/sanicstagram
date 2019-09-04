from marshmallow import Schema, fields


class TagSchema(Schema):
    name = fields.Str()


class CommentSchema(Schema):
    id = fields.Int()
    body = fields.Str()
    creator = fields.Method('get_creator')
    tags = fields.List(fields.Nested(TagSchema))

    def get_creator(self, obj):
        return obj.creator.nickname


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
    tags = fields.Method('get_tags')

    def get_tags(self, obj):
        return [
            tag.name
            for tag in obj.tags
        ]


class FeedViewPostResponseSchema(PostSchema):
    attachments = fields.List(fields.Nested(AttachmentSchema))
    comments = fields.List(fields.Nested(CommentSchema))
    tags = fields.Method('get_tags')
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    def get_tags(self, obj):
        if not obj or not obj.tags:
            return []
        return [
            tag.name
            for tag in obj.tags
        ]


class CreateCommentResponseSchema(PostSchema):
    id = fields.Int()
    body = fields.Str()
    creator = fields.Str()
