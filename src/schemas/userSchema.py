from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    name = fields.Str(required=True, validate=lambda n: len(n) >= 3)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True, validate=lambda p: len(p) >= 8)