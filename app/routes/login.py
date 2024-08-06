# 导入所需的模块
from flask import Blueprint, request, jsonify
from webargs.flaskparser import use_args
from datetime import datetime
import secrets
from ..models import User, Role, db
from ..database.user_db_operations import get_user_info_by_username, get_role_info_by_username
from ..schema import loginSchema

# 定义蓝图
bp = Blueprint('login', __name__)


# 登录路由
@bp.route('/login', methods=['POST'])
@use_args(loginSchema(), location='json')
def login(args):
    username = args['username']
    password = args['password']

    # 查询数据库以验证用户名和密码
    user = User.query.filter_by(username=username).first()
    if user and user.password_hash == password:  # 假设密码直接存储，实际中应使用哈希比较
        user_info = get_user_info_by_username(username)
        role_info = get_role_info_by_username(username)

        # 生成随机 token
        token = secrets.token_hex(16)  # 生成32个字符的随机token

        # 构建响应数据
        response_data = {
            "code": 200,
            "msg": "登录成功",
            "username": user_info["username"],
            "nickName": role_info["role_name"] if role_info else None,
            "userID": user_info["id"],
            "roleID": role_info["id"] if role_info else None,
            "token": token,
            "roles": [
                {
                    "roleCode": role_info["role_code"] if role_info else None,
                    "roleId": role_info["id"] if role_info else None,
                    "roleName": role_info["role_name"] if role_info else None
                }
            ],
            "data": datetime.now().isoformat()
        }

        return jsonify(response_data)
    else:
        return jsonify({"error": "无效的凭据"}), 401