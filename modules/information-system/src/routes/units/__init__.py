from flask import Blueprint

module_name = 'units'
bp = Blueprint(module_name, __name__)

from src.routes.units import index
from src.routes.units import add
from src.routes.units import edit