from marshmallow import Schema, fields


class CreateArticleRequestSchema(Schema):
    pw = fields.Str()
    subject = fields.Str()
    content = fields.Str()


class GetArticleListResponseSchema(Schema):
    id = fields.Int()
    subject = fields.Str()
    content = fields.Str()
