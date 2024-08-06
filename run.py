from app import create_app
from app.routes import bp 
from flask_cors import CORS
from app.database import init_db

app= create_app()
CORS(app)
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
        # 在应用上下文中初始化数据库
    with app.app_context():
        init_db()