from marshmallow import Schema, fields


class GetUserRequestSchema(Schema):
    nickname = fields.Str(required=True)


class RegisterUserRequestSchema(Schema):
    pass


class GetUserListRequestSchema(Schema):
    pass


class UpdateUserRequestSchema(Schema):
    pass


class SearchUserRequestSchema(Schema):
    nickname = fields.Str(required=True)
