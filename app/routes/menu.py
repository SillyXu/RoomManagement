from flask import Blueprint, request, jsonify
from webargs.flaskparser import use_args
from marshmallow import Schema, fields
from flask_cors import CORS, cross_origin

class MenuSchema(Schema):
    menuUrl = fields.Str()
    menuName = fields.Str()
    icon = fields.Str()
    tip = fields.Str()
    parentPath = fields.Str()
    children = fields.List(fields.Dict())

bp = Blueprint('menu', __name__)

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

    if user_id is not None and role_id is not None:
        return jsonify(return_value)
    else:
        return jsonify({"error": "Invalid parameters"}), 400