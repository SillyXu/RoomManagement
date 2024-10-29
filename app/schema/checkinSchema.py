from marshmallow import Schema, fields, ValidationError

class CheckinSchema(Schema):
    """入住记录模式定义"""

    occupant_name = fields.Str(required=True, description="入住人姓名")
    employee_id = fields.Int(required=True, description="员工ID")
    room_number = fields.Int(required=True, description="房间号")
    reason = fields.Str(required=True, description="入住原因")
    checkin_date = fields.DateTime(required=True, format='%Y-%m-%d', description="入住日期")
    checkout_date = fields.DateTime(required=False, format='%Y-%m-%d', description="退房日期")
    checkin_id = fields.Int(required=False, description="入住ID")

    def validate_data(self, data):
        """验证入住记录数据"""
        try:
            self.load(data)
        except ValidationError as err:
            raise ValueError("Invalid check-in data") from err

# 创建 CheckinSchema 的实例
checkin_args = CheckinSchema()