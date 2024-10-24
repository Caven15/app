from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Integer(required=True)
    username = fields.String(required=True, validate=validate.Length(min=5))
    email = fields.Email(required=True, validate=validate.Email())
