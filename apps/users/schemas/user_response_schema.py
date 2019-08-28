from marshmallow import Schema, fields


class ExploreUsersResponseSchema(Schema):
    id = fields.Int()
    profile_image = fields.Str()
    name = fields.Str()
