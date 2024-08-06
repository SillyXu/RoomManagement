# room_db_operations.py
from ..models import Room, db

def create_room(room_data):
    """创建一个新的房间记录"""
    new_room = Room(
        room_name=room_data['room_name'],
        floor=room_data['floor'],
        room_number=room_data['room_number'],
        room_type=room_data['room_type'],
        room_capacity=room_data['room_capacity'],
        room_price=room_data['room_price'],
        room_status=room_data['room_status'],
        room_image=room_data.get('room_image')  # 可选字段
    )
    db.session.add(new_room)
    db.session.commit()
    return new_room

def get_room_by_number(room_number):
    """通过房间号获取房间信息"""
    return Room.query.filter_by(room_number=room_number).first()

def update_room(room_number, room_data):
    """更新房间信息"""
    room = get_room_by_number(room_number)
    if room:
        for key, value in room_data.items():
            setattr(room, key, value)
        db.session.commit()
        return room
    return None

def delete_room(room_number):
    """删除房间记录"""
    room = get_room_by_number(room_number)
    if room:
        db.session.delete(room)
        db.session.commit()
        return True
    return False

def get_all_rooms():
    """获取所有房间的信息"""
    return Room.query.all()

def get_rooms_by_status(status):
    """根据状态获取房间列表"""
    return Room.query.filter_by(room_status=status).all()

def get_rooms_by_floor(floor):
    """根据楼层获取房间列表"""
    return Room.query.filter_by(floor=floor).all()