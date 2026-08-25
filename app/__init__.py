import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

login_manager.login_view = 'auth.login'
login_manager.login_message = 'يرجى تسجيل الدخول للمتابعة'
login_manager.login_message_category = 'warning'

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config and isinstance(test_config, dict):
        app.config.from_mapping(test_config)
    else:
        env = test_config if isinstance(test_config, str) else os.environ.get('FLASK_ENV', 'development')
        app.config.from_object(config[env])

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.blueprints.auth import auth_bp
    from app.blueprints.main import main_bp
    from app.blueprints.employees import emp_bp
    from app.blueprints.settings import settings_bp
    from app.blueprints.reports import reports_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(emp_bp, url_prefix='/employees')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    app.register_blueprint(reports_bp, url_prefix='/reports')

    from app.blueprints.main.routes import register_error_handlers
    register_error_handlers(app)

    return app
