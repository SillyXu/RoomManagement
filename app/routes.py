from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from . import db
from .models import Room

bp = Blueprint('routes', __name__)

@bp.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([room.to_dict() for room in rooms])


@bp.route('/api/rooms', methods=['POST'])
def create_room():
    data = request.form
    image = request.files['image']
    filename = secure_filename(image.filename)
    image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    new_room = Room(type=data['type'], image_path=filename)
    db.session.add(new_room)
    db.session.commit()
    return jsonify(new_room.to_dict()), 201


@bp.route('/api/upload/<filename>', methods=['POST'])
def upload_image(filename):
    file = request.files['file']
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return jsonify({'message': f'Image {filename} uploaded successfully.'})


@bp.route('/static/images/<filename>')
def serve_image(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@bp.route('/')
def index():
    return "Welcome to the Hotel Management System"