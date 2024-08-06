# checkin_db_operations.py
from ..models import Checkins, db, Personnel, Room
from datetime import datetime

def create_checkin(checkin_data):
    """创建一个新的入住记录"""
    new_checkin = Checkins(
        occupant_name=checkin_data['occupant_name'],
        employee_id=checkin_data['employee_id'],
        room_number=checkin_data['room_number'],
        reason=checkin_data['reason'],
        checkin_date=datetime.strptime(checkin_data['checkin_date'], '%Y-%m-%d').date(),
        checkout_date=datetime.strptime(checkin_data.get('checkout_date', ''), '%Y-%m-%d').date() if checkin_data.get('checkout_date') else None
    )
    db.session.add(new_checkin)
    db.session.commit()
    return new_checkin

def get_checkin_by_id(checkin_id):
    """通过入住ID获取入住信息"""
    return Checkins.query.filter_by(checkin_id=checkin_id).first()

def update_checkin(checkin_id, checkin_data):
    """更新入住信息"""
    checkin = get_checkin_by_id(checkin_id)
    if checkin:
        for key, value in checkin_data.items():
            setattr(checkin, key, value)
        db.session.commit()
        return checkin
    return None

def delete_checkin(checkin_id):
    """删除入住记录"""
    checkin = get_checkin_by_id(checkin_id)
    if checkin:
        db.session.delete(checkin)
        db.session.commit()
        return True
    return False

def get_all_checkins():
    """获取所有入住信息"""
    return Checkins.query.all()

def get_checkins_by_employee(employee_id):
    """根据员工ID获取入住列表"""
    return Checkins.query.filter_by(employee_id=employee_id).all()

def get_checkins_by_room(room_number):
    """根据房间号获取入住列表"""
    return Checkins.query.filter_by(room_number=room_number).all()

def get_checkins_by_reason(reason):
    """根据入住原因获取入住列表"""
    return Checkins.query.filter_by(reason=reason).all()

def get_checkins_by_date(checkin_date):
    """根据入住日期获取入住列表"""
    return Checkins.query.filter(Checkins.checkin_date == checkin_date).all()