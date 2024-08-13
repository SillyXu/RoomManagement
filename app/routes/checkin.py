import logging
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from ..models import Checkins, db
from ..schema.checkinSchema import CheckinSchema
from webargs.flaskparser import use_args
from ..database.checkin_db_operations import (
    create_checkin,
    get_checkin_by_id,
    update_checkin,
    delete_checkin,
    get_all_checkins,
    get_checkins_by_employee,
    get_checkins_by_room,
    get_checkins_by_reason,
    get_checkins_by_date
)
from ..logger import get_logger

bp = Blueprint('checkin', __name__)

# 使用 CheckinSchema 进行数据验证
checkin_args = CheckinSchema()

# 创建日志实例
logger = get_logger(__name__, 'checkin.log')

@bp.route('/addCheckinInfo', methods=['POST', "OPTIONS"])
@cross_origin()
@use_args(checkin_args, location='json')
def add_checkin_info(args):
    """新建入住记录接口"""
    logger.info(f"Received request to add checkin info: {args}")
    try:
        new_checkin = create_checkin(args)
        logger.info(f"Checkin added successfully: {new_checkin.to_dict()}")
        return jsonify({"success": True, "message": "Checkin added successfully", "checkin": new_checkin.to_dict()}), 201
    except Exception as e:
        logger.error(f"Failed to add checkin: {str(e)}")
        return jsonify({"success": False, "error": str(e), "message": "Failed to add checkin"}), 500
    
@bp.route('/getCheckinInfo/<int:checkin_id>', methods=['GET'])
def get_checkin_info(checkin_id):
    """获取单个入住记录接口"""
    logger.info(f"Received request to get checkin info by ID: {checkin_id}")
    checkin = get_checkin_by_id(checkin_id)
    if checkin:
        logger.info(f"Checkin info retrieved: {checkin.to_dict()}")
        return jsonify({"success": True, "message": "Checkin info retrieved", "checkin": checkin.to_dict()})
    logger.warning(f"Checkin with ID {checkin_id} not found")
    return jsonify({"success": False, "error": "Checkin not found", "message": "Checkin not found"}), 404

@bp.route('/updateCheckinInfo/<int:checkin_id>', methods=['PUT'])
@use_args(checkin_args, location='json')
def update_checkin_info(args, checkin_id):
    """更新入住记录接口"""
    logger.info(f"Received request to update checkin info: {args} for ID: {checkin_id}")
    try:
        updated_checkin = update_checkin(checkin_id, args)
        if updated_checkin:
            logger.info(f"Checkin updated successfully: {updated_checkin.to_dict()}")
            return jsonify({"success": True, "message": "Checkin updated successfully", "checkin": updated_checkin.to_dict()})
        logger.warning(f"Checkin with ID {checkin_id} not found")
        return jsonify({"success": False, "error": "Checkin not found", "message": "Checkin not found"}), 404
    except Exception as e:
        logger.error(f"Failed to update checkin: {str(e)}")
        return jsonify({"success": False, "error": str(e), "message": "Failed to update checkin"}), 500

@bp.route('/deleteCheckin/<int:checkin_id>', methods=['DELETE'])
def delete_checkin_info(checkin_id):
    """删除入住记录接口"""
    logger.info(f"Received request to delete checkin info by ID: {checkin_id}")
    if delete_checkin(checkin_id):
        logger.info(f"Checkin with ID {checkin_id} deleted successfully")
        return jsonify({"success": True, "message": "Checkin deleted successfully"})
    logger.warning(f"Checkin with ID {checkin_id} not found")
    return jsonify({"success": False, "error": "Checkin not found", "message": "Checkin not found"}), 404

@bp.route('/getCheckinInfo', methods=['GET'])
def get_all_checkins_info():
    """获取所有入住记录接口"""
    logger.info("Received request to get all checkins")
    checkins = get_all_checkins()
    logger.info(f"All checkins retrieved: {[checkin.to_dict() for checkin in checkins]}")
    return jsonify({"success": True, "message": "All checkins retrieved", "checkins": [checkin.to_dict() for checkin in checkins]})

@bp.route('/getCheckinsByEmployee/<int:employee_id>', methods=['GET'])
def get_checkins_by_employee_info(employee_id):
    """根据员工ID获取入住记录列表接口"""
    logger.info(f"Received request to get checkins by employee ID: {employee_id}")
    checkins = get_checkins_by_employee(employee_id)
    logger.info(f"Checkins by employee ID {employee_id} retrieved: {[checkin.to_dict() for checkin in checkins]}")
    return jsonify({"success": True, "message": f"Checkins by employee ID {employee_id} retrieved", "checkins": [checkin.to_dict() for checkin in checkins]})

@bp.route('/getCheckinsByRoom/<int:room_number>', methods=['GET'])
def get_checkins_by_room_info(room_number):
    """根据房间号获取入住记录列表接口"""
    logger.info(f"Received request to get checkins by room number: {room_number}")
    checkins = get_checkins_by_room(room_number)
    logger.info(f"Checkins by room number {room_number} retrieved: {[checkin.to_dict() for checkin in checkins]}")
    return jsonify({"success": True, "message": f"Checkins by room number {room_number} retrieved", "checkins": [checkin.to_dict() for checkin in checkins]})

@bp.route('/getCheckinsByReason/<string:reason>', methods=['GET'])
def get_checkins_by_reason_info(reason):
    """根据入住原因获取入住记录列表接口"""
    logger.info(f"Received request to get checkins by reason: {reason}")
    checkins = get_checkins_by_reason(reason)
    logger.info(f"Checkins by reason {reason} retrieved: {[checkin.to_dict() for checkin in checkins]}")
    return jsonify({"success": True, "message": f"Checkins by reason {reason} retrieved", "checkins": [checkin.to_dict() for checkin in checkins]})

@bp.route('/getCheckinsByDate/<string:checkin_date>', methods=['GET'])
def get_checkins_by_date_info(checkin_date):
    """根据入住日期获取入住记录列表接口"""
    logger.info(f"Received request to get checkins by date: {checkin_date}")
    checkins = get_checkins_by_date(checkin_date)
    logger.info(f"Checkins by date {checkin_date} retrieved: {[checkin.to_dict() for checkin in checkins]}")
    return jsonify({"success": True, "message": f"Checkins by date {checkin_date} retrieved", "checkins": [checkin.to_dict() for checkin in checkins]})