import logging
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from ..models import Checkins, db
from ..schema.checkinSchema import CheckinSchema
from webargs.flaskparser import use_args
from ..database.checkin_db_operations import (
    checkout_checkin,
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

def make_response(code, message, data=None):
    response = {"code": code, "msg": message}
    if data:
        response["data"] = data
    return jsonify(response), code

@bp.route('/addCheckinInfo', methods=['POST', "OPTIONS"])
@cross_origin()
@use_args(checkin_args, location='json')
def add_checkin_info(args):
    """新建入住记录接口"""
    logger.info(f"Received request to add checkin info: {args}")
    try:
        # 假设入住记录的唯一性由 employee_id 和 checkin_date 确定
        existing_checkin = Checkins.query.filter_by(
            employee_id=args['employee_id'], 
            checkin_date=args['checkin_date']
        ).first()

        if existing_checkin:
            # 如果存在重复记录，则返回错误
            return make_response(500, "Checkin already exists for the same employee and date")

        new_checkin = create_checkin(args)
        logger.info(f"Checkin added successfully: {new_checkin.to_dict()}")
        return make_response(200, "Checkin added successfully", new_checkin.to_dict())
    except Exception as e:
        logger.error(f"Failed to add checkin: {str(e)}")
        return make_response(500, "Failed to add checkin", str(e))

@bp.route('/getCheckinInfo/<int:checkin_id>', methods=['GET'])
def get_checkin_info(checkin_id):
    """获取单个入住记录接口"""
    logger.info(f"Received request to get checkin info by ID: {checkin_id}")
    checkin = get_checkin_by_id(checkin_id)
    if checkin:
        logger.info(f"Checkin info retrieved: {checkin.to_dict()}")
        return make_response(200, "Checkin info retrieved", checkin.to_dict())
    logger.warning(f"Checkin with ID {checkin_id} not found")
    return make_response(404, "Checkin not found")

@bp.route('/updateCheckinInfo', methods=['POST'])
@cross_origin()
@use_args(checkin_args, location='json')
def update_checkin_info(args):
    """更新入住记录接口"""
    checkin_id = args.get('checkin_id')
    logger.info(f"Received request to update checkin info: {args} for ID: {checkin_id}")
    try:
        updated_checkin = update_checkin(checkin_id, args)
        if updated_checkin:
            logger.info(f"Checkin updated successfully: {updated_checkin.to_dict()}")
            return make_response(200, "Checkin updated successfully", updated_checkin.to_dict())
        logger.warning(f"Checkin with ID {checkin_id} not found")
        return make_response(404, "Checkin not found")
    except Exception as e:
        logger.error(f"Failed to update checkin: {str(e)}")
        return make_response(500, "Failed to update checkin", str(e))

@bp.route('/deleteCheckin', methods=['POST'])
@cross_origin()
def delete_checkin_info():
    """删除入住记录接口"""
    checkin_id = request.json.get('checkin_id')
    logger.info(f"Received request to delete checkin info by ID: {checkin_id}")
    if delete_checkin(checkin_id):
        logger.info(f"Checkin with ID {checkin_id} deleted successfully")
        return make_response(200, "Checkin deleted successfully")
    logger.warning(f"Checkin with ID {checkin_id} not found")
    return make_response(404, "Checkin not found")

@bp.route('/checkoutCheckin', methods=['POST'])
@cross_origin()
def checkout_checkin_info():
    """处理退房操作接口"""
    checkin_data = request.json
    logger.info(f"Received request to checkout checkin: {checkin_data}")
    try:
        result = checkout_checkin(checkin_data)
        if isinstance(result, str):
            return make_response(500, result)
        logger.info(f"Checkin checked out successfully: {result.to_dict()}")
        return make_response(200, "Checkin checked out successfully", result.to_dict())
    except Exception as e:
        logger.error(f"Failed to checkout checkin: {str(e)}")
        return make_response(500, "Failed to checkout checkin", str(e))

@bp.route('/getCheckinInfo', methods=['GET'])
@cross_origin()
def get_all_checkins_info():
    """获取所有入住记录接口"""
    logger.info("Received request to get all checkins")

    # 从请求参数中获取 is_historical
    is_historical = request.args.get('is_historical')
    if is_historical is not None:
        is_historical = int(is_historical)

    try:
        checkins = get_all_checkins(is_historical)
        logger.info(f"All checkins retrieved: {[checkin.to_dict() for checkin in checkins]}")
        return make_response(200, "All checkins retrieved", [checkin.to_dict() for checkin in checkins])
    except ValueError as e:
        logger.error(f"Invalid is_historical value: {is_historical}")
        return make_response(400, str(e), [])
    except Exception as e:
        logger.error(f"Error retrieving checkins: {e}")
        return make_response(500, "Internal Server Error", [])

@bp.route('/getCheckinsByEmployee/<int:employee_id>', methods=['GET'])
def get_checkins_by_employee_info(employee_id):
    """根据员工ID获取入住记录列表接口"""
    logger.info(f"Received request to get checkins by employee ID: {employee_id}")
    checkins = get_checkins_by_employee(employee_id)
    logger.info(f"Checkins by employee ID {employee_id} retrieved: {[checkin.to_dict() for checkin in checkins]}")
    return make_response(200, f"Checkins by employee ID {employee_id} retrieved", [checkin.to_dict() for checkin in checkins])

@bp.route('/getCheckinsByRoom/<int:room_number>', methods=['GET'])
def get_checkins_by_room_info(room_number):
    """根据房间号获取入住记录列表接口"""
    logger.info(f"Received request to get checkins by room number: {room_number}")
    checkins = get_checkins_by_room(room_number)
    logger.info(f"Checkins by room number {room_number} retrieved: {[checkin.to_dict() for checkin in checkins]}")
    return make_response(200, f"Checkins by room number {room_number} retrieved", [checkin.to_dict() for checkin in checkins])

@bp.route('/getCheckinsByReason/<string:reason>', methods=['GET'])
def get_checkins_by_reason_info(reason):
    """根据入住原因获取入住记录列表接口"""
    logger.info(f"Received request to get checkins by reason: {reason}")
    checkins = get_checkins_by_reason(reason)
    logger.info(f"Checkins by reason {reason} retrieved: {[checkin.to_dict() for checkin in checkins]}")
    return make_response(200, f"Checkins by reason {reason} retrieved", [checkin.to_dict() for checkin in checkins])

@bp.route('/getCheckinsByDate/<string:checkin_date>', methods=['GET'])
def get_checkins_by_date_info(checkin_date):
    """根据入住日期获取入住记录列表接口"""
    logger.info(f"Received request to get checkins by date: {checkin_date}")
    checkins = get_checkins_by_date(checkin_date)
    logger.info(f"Checkins by date {checkin_date} retrieved: {[checkin.to_dict() for checkin in checkins]}")
    return make_response(200, f"Checkins by date {checkin_date} retrieved", [checkin.to_dict() for checkin in checkins])