from flask import Blueprint

module_name = 'events'
bp = Blueprint(module_name, __name__)

from src.routes.events import index
from src.routes.events import add
from src.routes.events import edit