# routes/room.py
from sqlite3 import IntegrityError
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from ..models import Room, db
from ..schema.roomSchema import RoomSchema
from marshmallow.exceptions import ValidationError
from webargs.flaskparser import use_args
from flask_cors import CORS, cross_origin
from ..database.room_db_operations import (
    create_room,
    room_exists,
    upload_room_image,
    get_room_by_number,
    update_room,
    delete_room,
    get_all_rooms,
    get_rooms_by_status,
    get_rooms_by_floor
)
# 导入日志模块
from ..logger import get_logger

# 创建日志实例
logger = get_logger(__name__, 'room.log')

bp = Blueprint('room', __name__)

# 使用 RoomSchema 进行数据验证
room_args = RoomSchema()

def make_response(code, message, data=None):
    response = {"code": code, "msg": message}
    if data:
        response["data"] = data
    return jsonify(response), code

@bp.route('/addRoomInfo', methods=['POST'])
@cross_origin()
@use_args(room_args, location='json')
def add_room_info(args):
    """新建房间接口"""
    try:
        new_room = Room(
            room_name=args['room_name'],
            floor=args['floor'],
            room_number=args['room_number'],
            room_type=args['room_type'],
            room_capacity=args['room_capacity'],
            room_price=args['room_price'],
            room_status=args['room_status'],
            room_image_path=args.get('room_image_path')
        )
        db.session.add(new_room)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()  # 回滚事务
        if 'UNIQUE constraint failed' in str(e):
            return make_response(203, "房间号已存在")
        return make_response(500, "数据库错误")
    except Exception as e:
        db.session.rollback()  # 回滚事务
        return make_response(500, str(e))
    
    return make_response(200, "房间添加成功")
@bp.route('/getRoomInfo/<string:room_number>', methods=['GET'])
def get_room_info(room_number):
    """获取单个房间信息接口"""
    logger.info(f"Received request to get room info for room number {room_number}.")
    room = get_room_by_number(room_number)
    if room:
        logger.info(f"Room found: {room.to_dict()}")
        return make_response(200, "Room found", room.to_dict())
    logger.warning(f"Room not found for room number {room_number}.")
    return make_response(404, "Room not found")

@bp.route('/updateRoomInfo', methods=['POST'])
@cross_origin()
@use_args(room_args, location='json')
def update_room_info(args):
    """更新房间信息接口"""
    room_number = args.get('room_number')  # 获取房间号
    logger.info(f"Received request to update room info for room number {room_number}: {args}")
    
    try:
        updated_room = update_room(room_number, args)
        if updated_room:
            logger.info(f"Room updated successfully: {updated_room.to_dict()}")
            return make_response(200, "Room updated successfully", updated_room.to_dict())
        logger.warning(f"Room not found for room number {room_number}.")
        return make_response(404, "Room not found")
    except ValidationError as e:
        logger.error(f"Validation error: {e.messages}")
        return make_response(400, "输入数据无效", e.messages)
    except Exception as e:
        logger.error(f"Failed to update room: {str(e)}")
        return make_response(500, "Failed to update room", str(e))

@bp.route('/deleteRoom', methods=['POST'])
@cross_origin()
def delete_room_info():
    """删除房间接口"""
    room_number = request.json.get('room_number')  # 获取房间号
    logger.info(f"Received request to delete room for room number {room_number}.")
    if delete_room(room_number):
        logger.info(f"Room deleted successfully for room number {room_number}.")
        return make_response(200, "Room deleted successfully")
    logger.warning(f"Room not found for room number {room_number}.")
    return make_response(404, "Room not found")

@bp.route('/getAllRooms', methods=['GET'])
@cross_origin()
def get_all_rooms_info():
    """获取所有房间信息接口"""
    logger.info("Received request to get all rooms info.")
    rooms = get_all_rooms()
    logger.info(f"All rooms retrieved: {[room.to_dict() for room in rooms]}")
    return make_response(200, "All rooms retrieved", [room.to_dict() for room in rooms])

@bp.route('/getRoomsByStatus/<string:status>', methods=['GET'])
def get_rooms_by_status_info(status):
    """根据状态获取房间列表接口"""
    logger.info(f"Received request to get rooms by status: {status}.")
    rooms = get_rooms_by_status(status)
    logger.info(f"Rooms by status retrieved: {[room.to_dict() for room in rooms]}")
    return make_response(200, f"Rooms by status '{status}' retrieved", [room.to_dict() for room in rooms])

@bp.route('/getRoomsByFloor/<int:floor>', methods=['GET'])
def get_rooms_by_floor_info(floor):
    """根据楼层获取房间列表接口"""
    logger.info(f"Received request to get rooms by floor: {floor}.")
    rooms = get_rooms_by_floor(floor)
    logger.info(f"Rooms by floor retrieved: {[room.to_dict() for room in rooms]}")
    return make_response(200, f"Rooms by floor '{floor}' retrieved", [room.to_dict() for room in rooms])