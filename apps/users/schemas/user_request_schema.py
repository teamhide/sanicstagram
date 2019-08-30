from marshmallow import Schema, fields


class GetUserRequestSchema(Schema):
    name = fields.Str(required=True)


class RegisterUserRequestSchema(Schema):
    pass


class GetUserListRequestSchema(Schema):
    pass


class UpdateUserRequestSchema(Schema):
    pass
