from flask import Blueprint, request, jsonify
from webargs.flaskparser import use_args, parser
from marshmallow import Schema, fields, ValidationError
from flask_cors import CORS, cross_origin
from ..utils.error_handlers import handle_validation_error

# 定义蓝图
bp = Blueprint('menu', __name__)

# 定义菜单项的数据验证模式
class MenuSchema(Schema):
    menuUrl = fields.Str()
    menuName = fields.Str()
    icon = fields.Str()
    tip = fields.Str()
    parentPath = fields.Str()
    children = fields.List(fields.Dict())

# 示例菜单数据
admin_routes = [
    {
        "menuUrl": "/roomManagement",
        "menuName": "房间管理",
        "icon": "SettingIcon",
        "tip": "new",
        "parentPath": "",
        "children": [
            {
                "parentPath": "/roomManagement",
                "menuUrl": "/roomManagement/apartmentList",
                "menuName": "房间列表",
            },
            {
                "parentPath": "/roomManagement",
                "menuUrl": "/roomManagement/apartmentView",
                "menuName": "房间概况",
            },
            {
                "parentPath": "/roomManagement",
                "menuUrl": "/roomManagement/apartmentAdd",
                "menuName": "新增房型",
                "cacheable": True,
            },
        ],
    },
    {
        "menuUrl": "/peopleManagement",
        "menuName": "人员管理",
        "icon": "SettingIcon",
        "tip": "dot",
        "parentPath": "",
        "children": [
            {
                "parentPath": "/peopleManagement",
                "menuUrl": "/peopleManagement/peopleAdd",
                "menuName": "入住登记",
            },
            {
                "parentPath": "/peopleManagement",
                "menuUrl": "/peopleManagement/peopleList",
                "menuName": "入住信息",
            },
        ],
    },
]

# 返回值
return_value = {
    "code": 200,
    "msg": "获取菜单列表成功",
    "data": admin_routes,
}

@bp.route('/getMenuListByRoleId', methods=['POST', 'OPTIONS'])
@cross_origin()
def get_menu_list_by_role_id():
    if request.method == 'OPTIONS':
        return '', 204  # 返回空响应，状态码为 204

    data = request.get_json()
    user_id = data.get('userId', None)
    role_id = data.get('roleId', None)

    # 验证 userId 和 roleId 是否为整数
    if not (isinstance(user_id, int) and isinstance(role_id, int)):
        return jsonify({"error": "User ID and Role ID must be integers"}), 400

    if user_id is not None and role_id is not None:
        return jsonify(return_value)
    else:
        return jsonify({"error": "Invalid parameters"}), 400

# 自定义错误处理器
@parser.error_handler
def custom_error_handler(err, req, schema, *, error_status_code, error_headers):
    handle_validation_error(err, error_status_code)