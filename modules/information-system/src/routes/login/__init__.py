from flask import Blueprint

bp = Blueprint('login', __name__)

from src.routes.login import index