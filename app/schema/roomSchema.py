# schemas/room_schema.py
from marshmallow import Schema, fields, ValidationError

class RoomSchema(Schema):
    room_name = fields.Str(required=True)
    floor = fields.Int(required=True)
    room_number = fields.Str(required=True)
    room_type = fields.Str(required=True)
    room_capacity = fields.Int(required=True)
    room_price = fields.Int(required=True)
    room_status = fields.Str(required=True, validate=lambda n: n in ["空闲", "使用中", "维修中", "报废"])
    room_image = fields.Raw(required=False)

    class Meta:
        ordered = True

room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)