from . import db
from sqlalchemy import CheckConstraint


# 角色模型
class Role(db.Model):
    role_id = db.Column(db.Integer, autoincrement=True, unique=True)
    role_code = db.Column(db.String(10), primary_key=True, nullable=False)
    role_name = db.Column(db.String(100), nullable=False)

# 用户模型，与角色模型关联
class User(db.Model):
    user_id = db.Column(db.Integer, autoincrement=True, unique=True)
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_code = db.Column(db.String(10), db.ForeignKey('role.role_code'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy='dynamic'))

# 人员模型
class Personnel(db.Model):
    name = db.Column(db.String(100), nullable=False)
    employee_id = db.Column(db.String(100), primary_key=True, nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    department_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    __table_args__ = (
        db.CheckConstraint('gender IN ("男", "女")', name='gender_check'),
    )


# 备品信息模型
class SpareParts(db.Model):
    name = db.Column(db.String(100), nullable=False)
    part_number = db.Column(db.String(100), unique=True, primary_key=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    entry_date = db.Column(db.Date, nullable=False)
    last_inspection_date = db.Column(db.Date)
    status = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    __table_args__ = (
        db.CheckConstraint('status IN ("可用", "待检", "维修中", "报废")', name='status_check'),
    )

# 房间模型
class Room(db.Model):
    room_name = db.Column(db.String(100), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    room_number = db.Column(db.String(100), unique=True, primary_key=True, nullable=False)
    room_type = db.Column(db.String(100), nullable=False)
    room_capacity = db.Column(db.Integer, nullable=False)
    room_price = db.Column(db.Integer, nullable=False)
    room_status = db.Column(db.String(100), nullable=False)
    room_image_path = db.Column(db.String(255))
    __table_args__ = (
        db.CheckConstraint('room_status IN ("空闲", "使用中", "维修中", "报废")', name='room_status_check'),
    )

# 入住信息模型
class Checkins(db.Model):
    checkin_id = db.Column(db.Integer, primary_key=True)
    occupant_name = db.Column(db.String(100), nullable=False)
    employee_id = db.Column(db.String(100), db.ForeignKey('personnel.employee_id'), nullable=False)
    room_number = db.Column(db.String(100), db.ForeignKey('room.room_number'), nullable=False)
    reason = db.Column(db.String(100), nullable=False)
    checkin_date = db.Column(db.Date, nullable=False)
    checkout_date = db.Column(db.Date)
    __table_args__ = (
        db.CheckConstraint('reason IN ("因公", "因私")', name='reason_check'),
    )