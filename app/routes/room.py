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

bp = Blueprint('room', __name__)

# 使用 RoomSchema 进行数据验证
room_args = RoomSchema()

@bp.route('/addRoomInfo', methods=['POST'])
@use_args(room_args, location='json')
def add_room_info(args):
    """新建房间接口"""
    try:
        new_room = create_room(args)
        return jsonify({"message": "Room added successfully", "room": new_room.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@bp.route('/uploadRoomImage', methods=['POST'])
def upload_room_image_api():
    """API 用于上传房间图片"""
    if 'room_number' not in request.form or 'image' not in request.files:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    room_number = request.form['room_number']
    image_file = request.files['image']

    try:
        # 调用上传图片的方法
        upload_room_image(room_number, image_file)
        return jsonify({'message': 'Image uploaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/getRoomInfo/<string:room_number>', methods=['GET'])
def get_room_info(room_number):
    """获取单个房间信息接口"""
    room = get_room_by_number(room_number)
    if room:
        return jsonify({"room": room.to_dict()})
    return jsonify({"error": "Room not found"}), 404

@bp.route('/updateRoomInfo/<string:room_number>', methods=['PUT'])
@use_args(room_args, location='json')
def update_room_info(args, room_number):
    """更新房间信息接口"""
    try:
        updated_room = update_room(room_number, args)
        if updated_room:
            return jsonify({"message": "Room updated successfully", "room": updated_room.to_dict()})
        return jsonify({"error": "Room not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/deleteRoom/<string:room_number>', methods=['DELETE'])
def delete_room_info(room_number):
    """删除房间接口"""
    if delete_room(room_number):
        return jsonify({"message": "Room deleted successfully"})
    return jsonify({"error": "Room not found"}), 404

@bp.route('/getAllRooms', methods=['GET'])
def get_all_rooms_info():
    """获取所有房间信息接口"""
    rooms = get_all_rooms()
    return jsonify({"rooms": [room.to_dict() for room in rooms]})

@bp.route('/getRoomsByStatus/<string:status>', methods=['GET'])
def get_rooms_by_status_info(status):
    """根据状态获取房间列表接口"""
    rooms = get_rooms_by_status(status)
    return jsonify({"rooms": [room.to_dict() for room in rooms]})

@bp.route('/getRoomsByFloor/<int:floor>', methods=['GET'])
def get_rooms_by_floor_info(floor):
    """根据楼层获取房间列表接口"""
    rooms = get_rooms_by_floor(floor)
    return jsonify({"rooms": [room.to_dict() for room in rooms]})