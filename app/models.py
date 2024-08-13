from . import db
from sqlalchemy import CheckConstraint


# 角色模型
class Role(db.Model):
    role_id = db.Column(db.Integer, autoincrement=True, unique=True)
    role_code = db.Column(db.String(10), primary_key=True, nullable=False)
    role_name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        """将 Role 对象转换为字典"""
        return {
            'role_id': self.role_id,
            'role_code': self.role_code,
            'role_name': self.role_name
        }

# 用户模型，与角色模型关联
class User(db.Model):
    user_id = db.Column(db.Integer, autoincrement=True, unique=True)
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_code = db.Column(db.String(10), db.ForeignKey('role.role_code'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy='dynamic'))

    def to_dict(self):
        """将 User 对象转换为字典"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password_hash': self.password_hash,
            'role_code': self.role_code
        }

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

    def to_dict(self):
        """将 Personnel 对象转换为字典"""
        return {
            'name': self.name,
            'employee_id': self.employee_id,
            'company_name': self.company_name,
            'department_name': self.department_name,
            'position': self.position,
            'rank': self.rank,
            'age': self.age,
            'gender': self.gender
        }

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

    def to_dict(self):
        """将 SpareParts 对象转换为字典"""
        return {
            'name': self.name,
            'part_number': self.part_number,
            'quantity': self.quantity,
            'entry_date': self.entry_date.isoformat() if self.entry_date else None,
            'last_inspection_date': self.last_inspection_date.isoformat() if self.last_inspection_date else None,
            'status': self.status,
            'location': self.location
        }

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

    def to_dict(self):
        """将 Room 对象转换为字典"""
        return {
            'room_name': self.room_name,
            'floor': self.floor,
            'room_number': self.room_number,
            'room_type': self.room_type,
            'room_capacity': self.room_capacity,
            'room_price': self.room_price,
            'room_status': self.room_status,
            'room_image_path': self.room_image_path
        }

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

    def to_dict(self):
        """将 Checkins 对象转换为字典"""
        return {
            'checkin_id': self.checkin_id,
            'occupant_name': self.occupant_name,
            'employee_id': self.employee_id,
            'room_number': self.room_number,
            'reason': self.reason,
            'checkin_date': self.checkin_date.isoformat() if self.checkin_date else None,
            'checkout_date': self.checkout_date.isoformat() if self.checkout_date else None
        }