from marshmallow import Schema, fields, ValidationError

# 定义登录请求的数据验证模式
class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    def validate_username(self, value):
        if len(value) < 3:
            raise ValidationError("Username must be at least 3 characters long.")

    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")