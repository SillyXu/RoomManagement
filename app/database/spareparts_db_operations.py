# spareparts_db_operations.py
from ..models import SpareParts, db
from datetime import datetime

def create_spare_part(spare_part_data):
    """创建一个新的备品记录"""
    new_spare_part = SpareParts(
        name=spare_part_data['name'],
        part_number=spare_part_data['part_number'],
        quantity=spare_part_data['quantity'],
        entry_date=datetime.strptime(spare_part_data['entry_date'], '%Y-%m-%d').date(),
        last_inspection_date=datetime.strptime(spare_part_data.get('last_inspection_date', ''), '%Y-%m-%d').date() if spare_part_data.get('last_inspection_date') else None,
        status=spare_part_data['status'],
        location=spare_part_data['location']
    )
    db.session.add(new_spare_part)
    db.session.commit()
    return new_spare_part

def get_spare_part_by_part_number(part_number):
    """通过备品编号获取备品信息"""
    return SpareParts.query.filter_by(part_number=part_number).first()

def update_spare_part(part_number, spare_part_data):
    """更新备品信息"""
    spare_part = get_spare_part_by_part_number(part_number)
    if spare_part:
        for key, value in spare_part_data.items():
            setattr(spare_part, key, value)
        db.session.commit()
        return spare_part
    return None

def delete_spare_part(part_number):
    """删除备品记录"""
    spare_part = get_spare_part_by_part_number(part_number)
    if spare_part:
        db.session.delete(spare_part)
        db.session.commit()
        return True
    return False

def get_all_spare_parts():
    """获取所有备品的信息"""
    return SpareParts.query.all()

def get_spare_parts_by_status(status):
    """根据状态获取备品列表"""
    return SpareParts.query.filter_by(status=status).all()

def get_spare_parts_by_location(location):
    """根据位置获取备品列表"""
    return SpareParts.query.filter_by(location=location).all()

def get_spare_parts_by_entry_date(entry_date):
    """根据入库日期获取备品列表"""
    return SpareParts.query.filter(SpareParts.entry_date == entry_date).all()

def get_spare_parts_by_last_inspection_date(last_inspection_date):
    """根据最近一次检验日期获取备品列表"""
    return SpareParts.query.filter(SpareParts.last_inspection_date == last_inspection_date).all()