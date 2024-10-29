# checkin_db_operations.py
from ..models import Checkins, db, Personnel, Room
from datetime import datetime
from ..schema.checkinSchema import checkin_args

from ..logger import get_logger

# 创建日志实例
logger = get_logger(__name__, 'checkin.log')
def create_checkin(checkin_data):
    """创建一个新的入住记录"""
    # 查询房间状态
    room = Room.query.filter_by(room_number=checkin_data['room_number']).first()
    if not room:
        logger.warning("Room not found", room)
        return "房间不存在"

    # 根据房间类型判断空闲数量
    if room.room_type == "豪华间" and room.room_status != "空闲":
        logger.warning("豪华间已被占用", room)
        return "豪华间已占满"
    elif room.room_type == "标准间":
        occupied_count = Checkins.query.filter_by(room_number=room.room_number).count()
        if occupied_count >= 2:
            logger.warning("标准间已被占用", room)
            return "标准间已占满"

    # 更新房间状态
    room.room_status = "使用中"
    db.session.commit()

    # 确保日期时间字段是字符串格式
    checkin_data['checkin_date'] = checkin_data['checkin_date'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    if 'checkout_date' in checkin_data and checkin_data['checkout_date']:
        checkin_data['checkout_date'] = checkin_data['checkout_date'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # 创建入住记录
    new_checkin = Checkins(
        occupant_name=checkin_data['occupant_name'],
        employee_id=checkin_data['employee_id'],
        room_number=checkin_data['room_number'],
        reason=checkin_data['reason'],
        checkin_date=datetime.strptime(checkin_data['checkin_date'], '%Y-%m-%dT%H:%M:%S.%fZ'),
        checkout_date=datetime.strptime(checkin_data.get('checkout_date', ''), '%Y-%m-%dT%H:%M:%S.%fZ') if checkin_data.get('checkout_date') else None
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

def checkout_checkin(checkin_data):
    """处理退房操作"""
    checkin_id = checkin_data['checkin_id']
    print(f"checkin_data: {checkin_data}")  # 添加调试信息

    try:
        # 查询入住记录
        checkin = Checkins.query.filter_by(checkin_id=checkin_id, is_historical=0).first()
        if not checkin:
            logger.warning(f"No active checkin found for checkin_id: {checkin_id}")
            return "没有找到有效的入住记录"

        room_number = checkin.room_number

        # 查询房间
        room = Room.query.filter_by(room_number=room_number).first()
        if not room:
            logger.warning(f"Room not found: {room_number}")
            return "房间不存在"

        # 检查房间类型和是否有其他未退房的入住记录
        if room.room_type == "标准间":
            other_checkins = Checkins.query.filter_by(room_number=room_number, is_historical=0).filter(Checkins.checkin_id != checkin_id).all()
            if other_checkins:
                logger.info(f"Other checkins found for room {room_number}: {[c.checkin_id for c in other_checkins]}")
                # 不更新房间状态
                with db.session.begin_nested():
                    # 更新入住记录的 is_historical 字段
                    checkin.is_historical = 1
                db.session.commit()
                return checkin

        # 开始事务
        with db.session.begin_nested():
            # 更新房间状态
            room.room_status = "空闲"

            # 更新入住记录的 is_historical 字段
            checkin.is_historical = 1

        # 提交事务
        db.session.commit()

    except Exception as e:
        # 回滚事务
        db.session.rollback()
        logger.error(f"Error during checkout: {e}")
        return f"退房失败: {str(e)}"

    return checkin
def get_all_checkins(is_historical=0):
    """获取所有入住信息"""
    query = Checkins.query

    if is_historical is not None:
        if is_historical not in [0, 1]:
            raise ValueError("is_historical must be 0 or 1")
        query = query.filter_by(is_historical=is_historical)

    return query.all()

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