from marshmallow import Schema, fields, ValidationError

# 定义菜单项的数据验证模式
class MenuSchema(Schema):
    user_id = fields.Int(required=True)
    role_id = fields.Int(required=True)

    def validate_user_id(self, value):
        if len(value) < 1:
            raise ValidationError("Menu name cannot be empty.")

    def validate_role_id(self, value):
        if len(value) < 1:
            raise ValidationError("Path cannot be empty.")