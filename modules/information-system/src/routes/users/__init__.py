from flask import Blueprint

module_name = 'users'
bp = Blueprint(module_name, __name__)


from src.routes.users.add import add
from src.routes.users.index import index
from src.routes.users.edit import edit