from marshmallow import Schema, fields, validate

class UserDTO(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    jwt_token = fields.Str(dump_only=True)
