from flask import Blueprint

bp = Blueprint('admin', __name__)

from src.routes.admin import index