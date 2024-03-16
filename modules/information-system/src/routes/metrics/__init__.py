from flask import Blueprint

module_name = 'metrics'
bp = Blueprint(module_name, __name__)

from src.routes.metrics import index
from src.routes.metrics import add
from src.routes.metrics import edit