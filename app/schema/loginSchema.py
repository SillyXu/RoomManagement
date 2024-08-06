import re
from marshmallow import Schema, fields, ValidationError

# 定义登录请求的数据验证模式
class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    def validate_username(self, value):
        if len(value) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        
        # 验证 username 是否只包含字母、数字和下划线
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise ValidationError("Username contains invalid characters.")

    def validate_password(self, value):
        if len(value) < 5:
            raise ValidationError("Password must be at least 8 characters long.")
        
        # 验证 password 是否只包含字母、数字和特殊字符
        if not re.match(r'^[a-zA-Z0-9!@#$%^&*()-_=+]+$', value):
            raise ValidationError("Password contains invalid characters.")