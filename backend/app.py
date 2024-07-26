from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

# 初始化 Flask 应用和数据库
app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 设置最大上传文件大小

db = SQLAlchemy(app)

# 定义数据库模型
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), nullable=False)
    image_path = db.Column(db.String(200))
    # ... 其他字段

# 数据库初始化
with app.app_context():
    db.create_all()

# 房间列表路由
@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([room.to_dict() for room in rooms])

# 创建房间路由
@app.route('/api/rooms', methods=['POST'])
def create_room():
    data = request.form
    image = request.files['image']
    filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    new_room = Room(type=data['type'], image_path=filename)
    db.session.add(new_room)
    db.session.commit()
    return jsonify(new_room.to_dict()), 201

# 上传图片路由
@app.route('/api/upload/<filename>', methods=['POST'])
def upload_image(filename):
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({'message': f'Image {filename} uploaded successfully.'})

# 服务静态文件
@app.route('/static/images/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 主页路由（可选，用于测试）
@app.route('/')
def index():
    return "Welcome to the Hotel Management System"

if __name__ == '__main__':
    app.run(debug=True)