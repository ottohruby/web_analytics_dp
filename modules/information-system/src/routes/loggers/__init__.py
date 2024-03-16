from flask import Blueprint

module_name = 'loggers'
bp = Blueprint(module_name, __name__)

from src.routes.loggers import index
from src.routes.loggers import add
from src.routes.loggers import edit