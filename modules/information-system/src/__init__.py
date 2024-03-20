from flask import Flask, jsonify, render_template, redirect, flash
from src.config import Config
from flask_cors import CORS
from src.extensions.database import db
from src.models.user import User
from src.models.module_roles import ModuleRole
from src.models.user_roles import UserRole
from flask_login import current_user
from flask_login import login_required

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, max_age=3600)

    init_login_manager(app)
    init_database(app)

    # from flask_user import SQLAlchemyAdapter, UserManager
    # db_adapter = SQLAlchemyAdapter(db,  User)
    # user_manager = UserManager(db_adapter, app)
    init_cache(app)
    register_blueprints(app)

    

    return app

def init_login_manager(app):
    # from flask_login import LoginManager
    # login_manager = LoginManager()
    from src.extensions.login_manager import login_manager
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        flash('You are not authorized to access this page. Please log in.', 'warning')
        return redirect('/admin/login')

def init_database(app):
    db.init_app(app)

def init_cache(app):
    # from src.extensions.cache import cache
    # cache.init_app(app)
    return

def register_blueprints(app):
    from src.routes.admin import bp as admin_bp
    from src.routes.users import bp as users_bp
    from src.routes.events import bp as admin_event_bp
    from src.routes.dimensions import bp as admin_dimension_bp
    from src.routes.loggers import bp as admin_logger_bp
    from src.routes.metrics import bp as admin_metric_bp
    from src.routes.units import bp as admin_unit_bp

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(admin_event_bp, url_prefix='/events')
    app.register_blueprint(admin_dimension_bp, url_prefix='/dimensions')
    app.register_blueprint(admin_logger_bp, url_prefix='/loggers')
    app.register_blueprint(admin_metric_bp, url_prefix='/metrics')
    app.register_blueprint(admin_unit_bp, url_prefix='/units')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from src.routes.reports import bp as report_bp
    app.register_blueprint(report_bp, url_prefix='/reports')

    @app.route('/')
    @login_required
    def index():
        return render_template('index.html', 
                               modules=ModuleRole.get_available_modules(UserRole.get_active_role_ids(current_user.get_id())), 
                               title="Available Modules")

    @app.route('/healthy')
    def healthy():
        return jsonify({"message": "running"}), 200
    

