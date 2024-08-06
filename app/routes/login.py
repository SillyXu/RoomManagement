# 导入所需的模块
from flask import Blueprint, request, jsonify
from webargs.flaskparser import use_args, parser
from werkzeug.security import check_password_hash
from datetime import datetime
import secrets
from ..models import User, Role, db
from ..database.user_db_operations import get_user_info_by_username, get_role_info_by_username
from ..schema.loginSchema import LoginSchema
from flask_cors import CORS, cross_origin
from ..utils.error_handlers import handle_validation_error

# 定义蓝图
bp = Blueprint('login', __name__)

# 登录路由
@bp.route('/login', methods=['POST', "OPTIONS"])
@cross_origin()
@use_args(LoginSchema(), location='json')  # 修改use_args参数
def login(args):
    if request.method == "OPTIONS":
        # 返回一个简单的响应，状态码为 204
        return '', 204
    
    # 添加调试输出
    print("Received args:", args)

    username = args['username']
    password = args['password']

    # 查询数据库以验证用户名和密码
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):  # 使用check_password_hash进行验证
        user_info = get_user_info_by_username(username)
        role_info = get_role_info_by_username(username)

        # 生成随机 token
        token = secrets.token_hex(16)  # 生成32个字符的随机token

        # 构建响应数据
        response_data = {
            "code": 200,
            "msg": "登录成功",
            "data": {
                "nickName": role_info["role_name"] if role_info else None,
                "userName": user_info["username"],
                "userId": user_info["id"],
                "roleId": role_info["id"] if role_info else None,
                "token": token,
                "roles": [
                    {
                        "roleCode": role_info["role_code"] if role_info else None,
                        "roleId": role_info["id"] if role_info else None,
                        "roleName": role_info["role_name"] if role_info else None
                    }
                ]
            }
        }

        return jsonify(response_data)
    else:
        return jsonify({"error": "无效的凭据"}), 401

# 自定义错误处理器
@parser.error_handler
def custom_error_handler(err, error_status_code):
    handle_validation_error(err, error_status_code)