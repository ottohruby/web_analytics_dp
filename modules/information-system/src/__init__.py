from flask import Flask, jsonify, render_template
from src.config import Config
from flask_cors import CORS


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, max_age=3600)

    # Init extensions
    init_extensions(app)

    # Register blueprints
    register_blueprints(app)

    return app

def register_blueprints(app):
    from src.routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from src.routes.dashboards import bp as dashboards_bp
    app.register_blueprint(dashboards_bp, url_prefix='/dashboards')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/healthy')
    def healthy():
        return jsonify({"message": "running"}), 200

def init_extensions(app):
    from src.extensions.database import db
    db.init_app(app)