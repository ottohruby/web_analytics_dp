from flask import Flask, jsonify
from src.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init extensions
    init_extensions(app)

    # Register blueprints
    register_blueprints(app)

    return app

def register_blueprints(app):
    @app.route('/healthy')
    def healthy():
        return jsonify({"message": "running"}), 200

def init_extensions(app):
    pass