from flask import Blueprint

bp = Blueprint('dashboards', __name__)

from src.routes.dashboards import index