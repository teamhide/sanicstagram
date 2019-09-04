from marshmallow import Schema, fields


class BasePostResponseSchema(Schema):
    def get_tags(self, obj):
        if not obj or not obj.tags:
            return []
        return [
            tag.name
            for tag in obj.tags
        ]

    def get_creator(self, obj):
        return obj.creator.nickname


class TagSchema(BasePostResponseSchema):
    name = fields.String()


class CommentSchema(BasePostResponseSchema):
    id = fields.Integer()
    body = fields.String()
    creator = fields.Method('get_creator')
    tags = fields.List(fields.Nested(TagSchema))


class AttachmentSchema(BasePostResponseSchema):
    id = fields.Integer()
    path = fields.String()


class PostSchema(BasePostResponseSchema):
    id = fields.Integer()
    caption = fields.String()
    creator = fields.String()


class CreatePostResponseSchema(BasePostResponseSchema):
    id = fields.Integer()
    caption = fields.String()
    creator = fields.String()
    attachments = fields.List(fields.Nested(AttachmentSchema))
    comments = fields.List(fields.Nested(CommentSchema))
    tags = fields.Method('get_tags')


class FeedViewPostResponseSchema(BasePostResponseSchema):
    id = fields.Integer()
    caption = fields.String()
    creator = fields.String()
    attachments = fields.List(fields.Nested(AttachmentSchema))
    comments = fields.List(fields.Nested(CommentSchema))
    tags = fields.Method('get_tags')
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class CreateCommentResponseSchema(BasePostResponseSchema):
    id = fields.Integer()
    caption = fields.String()
    body = fields.String()
    creator = fields.String()


class PostDetailResponseSchema(BasePostResponseSchema):
    id = fields.Integer()
    caption = fields.String()
    creator = fields.String()
    attachments = fields.List(fields.Nested(AttachmentSchema))
    comments = fields.List(fields.Nested(CommentSchema))
    tags = fields.Method('get_tags')
    is_liked = fields.Boolean()
    like_count = fields.Integer()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
