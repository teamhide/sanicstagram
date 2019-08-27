from marshmallow import Schema, fields


class RegisterUserRequestSchema(Schema):
    pass


class GetUserListRequestSchema(Schema):
    pass


class UpdateUserRequestSchema(Schema):
    pass


class FollowUserRequestSchema(Schema):
    user_id = fields.Int(required=True)
    follow_user_id = fields.Int(required=True)


class UnFollowUserRequestSchema(Schema):
    user_id = fields.Int(required=True)
    follow_user_id = fields.Int(required=True)
