from marshmallow import Schema, fields, validate

class ProductDTO(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    amount = fields.Float(required=True)
    user_id = fields.Int(required=True)
