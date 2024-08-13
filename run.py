from app import create_app
from app.routes import bp 
from flask_cors import CORS
from app.database import init_db
from app.handler.roomHandler import init_error_handlers

app= create_app()
CORS(app)
app.register_blueprint(bp)
# 初始化错误处理
init_error_handlers(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
        # 在应用上下文中初始化数据库
    with app.app_context():
        init_db()