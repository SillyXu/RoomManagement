# routes/room.py
from flask import Blueprint, jsonify, request
from ..models import Room, db
from ..schema.roomSchema import RoomSchema
from webargs.flaskparser import use_args
from ..database.room_db_operations import (
    create_room,
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

@bp.route('/addRoomInfo', methods=['POST'])
@use_args(room_args, location='json')
def add_room_info(args):
    """新建房间接口"""
    logger.info(f"Received request to add room info: {args}")
    try:
        new_room = create_room(args)
        logger.info(f"Room added successfully: {new_room.to_dict()}")
        return jsonify({"message": "Room added successfully", "room": new_room.to_dict()}), 201
    except Exception as e:
        logger.error(f"Failed to add room: {str(e)}")
        return jsonify({"error": str(e), "message": "Failed to add room"}), 500
    
@bp.route('/uploadRoomImage', methods=['POST'])
def upload_room_image_api():
    """API 用于上传房间图片"""
    logger.info("Received request to upload room image.")
    if 'room_number' not in request.form or 'image' not in request.files:
        logger.warning("Missing required parameters for room image upload.")
        return jsonify({'error': 'Missing required parameters', 'message': 'Failed to upload image'}), 400
    
    room_number = request.form['room_number']
    image_file = request.files['image']

    try:
        # 调用上传图片的方法
        upload_room_image(room_number, image_file)
        logger.info(f"Image uploaded successfully for room number {room_number}.")
        return jsonify({'message': 'Image uploaded successfully'}), 200
    except Exception as e:
        logger.error(f"Failed to upload image: {str(e)}")
        return jsonify({'error': str(e), 'message': 'Failed to upload image'}), 500

@bp.route('/getRoomInfo/<string:room_number>', methods=['GET'])
def get_room_info(room_number):
    """获取单个房间信息接口"""
    logger.info(f"Received request to get room info for room number {room_number}.")
    room = get_room_by_number(room_number)
    if room:
        logger.info(f"Room found: {room.to_dict()}")
        return jsonify({"room": room.to_dict(), "message": "Room found"}), 200
    logger.warning(f"Room not found for room number {room_number}.")
    return jsonify({"error": "Room not found", "message": "Room not found"}), 404

@bp.route('/updateRoomInfo/<string:room_number>', methods=['PUT'])
@use_args(room_args, location='json')
def update_room_info(args, room_number):
    """更新房间信息接口"""
    logger.info(f"Received request to update room info for room number {room_number}: {args}")
    try:
        updated_room = update_room(room_number, args)
        if updated_room:
            logger.info(f"Room updated successfully: {updated_room.to_dict()}")
            return jsonify({"message": "Room updated successfully", "room": updated_room.to_dict()}), 200
        logger.warning(f"Room not found for room number {room_number}.")
        return jsonify({"error": "Room not found", "message": "Room not found"}), 404
    except Exception as e:
        logger.error(f"Failed to update room: {str(e)}")
        return jsonify({"error": str(e), "message": "Failed to update room"}), 500

@bp.route('/deleteRoom/<string:room_number>', methods=['DELETE'])
def delete_room_info(room_number):
    """删除房间接口"""
    logger.info(f"Received request to delete room for room number {room_number}.")
    if delete_room(room_number):
        logger.info(f"Room deleted successfully for room number {room_number}.")
        return jsonify({"message": "Room deleted successfully"}), 200
    logger.warning(f"Room not found for room number {room_number}.")
    return jsonify({"error": "Room not found", "message": "Room not found"}), 404

@bp.route('/getAllRooms', methods=['GET'])
def get_all_rooms_info():
    """获取所有房间信息接口"""
    logger.info("Received request to get all rooms info.")
    rooms = get_all_rooms()
    logger.info(f"All rooms retrieved: {[room.to_dict() for room in rooms]}")
    return jsonify({"rooms": [room.to_dict() for room in rooms], "message": "All rooms retrieved"}), 200

@bp.route('/getRoomsByStatus/<string:status>', methods=['GET'])
def get_rooms_by_status_info(status):
    """根据状态获取房间列表接口"""
    logger.info(f"Received request to get rooms by status: {status}.")
    rooms = get_rooms_by_status(status)
    logger.info(f"Rooms by status retrieved: {[room.to_dict() for room in rooms]}")
    return jsonify({"rooms": [room.to_dict() for room in rooms], "message": f"Rooms by status '{status}' retrieved"}), 200

@bp.route('/getRoomsByFloor/<int:floor>', methods=['GET'])
def get_rooms_by_floor_info(floor):
    """根据楼层获取房间列表接口"""
    logger.info(f"Received request to get rooms by floor: {floor}.")
    rooms = get_rooms_by_floor(floor)
    logger.info(f"Rooms by floor retrieved: {[room.to_dict() for room in rooms]}")
    return jsonify({"rooms": [room.to_dict() for room in rooms], "message": f"Rooms by floor '{floor}' retrieved"}), 200