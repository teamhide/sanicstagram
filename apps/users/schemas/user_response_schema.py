from marshmallow import Schema, fields


class ExploreUsersResponseSchema(Schema):
    id = fields.Int()
    profile_image = fields.Str()
    name = fields.Str()


class GetUserResponseSchema(Schema):
    name = fields.Str()
    profile_image = fields.Str()
    bio = fields.Str()
    website = fields.Str()
    followers_count = fields.Int()
    followings_count = fields.Int()
