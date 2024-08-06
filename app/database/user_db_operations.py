# database/db_operations.py
from .. import db
from ..models import Role, User, Personnel, SpareParts, Room, Checkins 
from werkzeug.security import generate_password_hash  # 导入密码哈希生成函数

def init_db():
    """初始化数据库"""
    db.create_all()  # 创建所有表

def seed_data():
    """插入种子数据"""
    # 检查超级管理员角色是否已存在
    admin_role = Role.query.filter_by(role_code='ROLE_admin').first()
    if not admin_role:
        admin_role = Role(role_id = 1, role_code='ROLE_admin', role_name='超级管理员')
        db.session.add(admin_role)
    
    # 检查管理员用户是否已存在
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        hashed_password = generate_password_hash('admin')  # 生成密码哈希
        admin_user = User(
            user_id = 1,
            username='admin',
            password_hash=hashed_password,  # 使用生成的密码哈希
            role_code='ROLE_admin'
        )
        db.session.add(admin_user)
    
    # 提交更改
    db.session.commit()

def add_role(role_code, role_name):
    """添加角色"""
    role = Role(role_code=role_code, role_name=role_name)
    db.session.add(role)
    db.session.commit()

def add_user(username, password, role_code):
    """添加用户"""
    hashed_password = generate_password_hash(password)
    user = User(username=username, password_hash=hashed_password, role_code=role_code)
    db.session.add(user)
    db.session.commit()

def get_all_roles():
    """获取所有角色"""
    roles = Role.query.all()
    return roles

def get_all_users():
    """获取所有用户"""
    users = User.query.all()
    return users

def delete_role(role_code):
    """删除角色"""
    role = Role.query.filter_by(role_code=role_code).first()
    if role:
        db.session.delete(role)
        db.session.commit()

def delete_user(username):
    """删除用户"""
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()

def get_user_info_by_username(username):
    """通过用户名获取用户信息"""
    user = User.query.filter_by(username=username).first()
    if user:
        return {
            "username": user.username,
            "role_code": user.role_code,
            "id": user.user_id
        }
    return None

def get_role_info_by_username(username):
    """通过用户名获取角色信息"""
    user = User.query.filter_by(username=username).first()
    if user:
        role = Role.query.filter_by(role_code=user.role_code).first()
        if role:
            return {
                "role_code": role.role_code,
                "role_name": role.role_name,
                "id": role.role_id
            }
    return None