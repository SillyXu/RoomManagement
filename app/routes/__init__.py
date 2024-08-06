from flask import Blueprint
from .menu import bp as menu_bp
from .login import bp as login_bp
from .index import bp as index_bp

bp = Blueprint('routes', __name__)

# 注册子蓝图
bp.register_blueprint(menu_bp)
bp.register_blueprint(login_bp)
bp.register_blueprint(index_bp)