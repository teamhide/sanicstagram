from marshmallow import Schema, fields


class RegisterUserRequestSchema(Schema):
    pass


class GetUserListRequestSchema(Schema):
    pass


class UpdateUserRequestSchema(Schema):
    pass


class FollowUserRequestSchema(Schema):
    follower_id = fields.Int()


class UnFollowUserRequestSchema(Schema):
    follower_id = fields.Int()
