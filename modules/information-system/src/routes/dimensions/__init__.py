from flask import Blueprint

module_name = 'dimensions'
bp = Blueprint(module_name, __name__)

from src.routes.dimensions.add import add
from src.routes.dimensions.index import index
from src.routes.dimensions.edit import edit
