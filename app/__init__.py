from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    from .errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # 添加 CLI 命令
    @app.cli.command("create-db")
    def create_db_command():
        """Create all tables in the database."""
        from .models import Role, User, Personnel, SpareParts, Room, Checkins  # 动态导入模型
        with app.app_context():
            db.create_all()
            print("Database tables created.")

    @app.cli.command("seed-db")
    def seed_db_command():
        """Seed the database with initial data."""
        from .database.user_db_operations import seed_data
        with app.app_context():
            seed_data()
            print("Database seeded with initial data.")
    
    return app
