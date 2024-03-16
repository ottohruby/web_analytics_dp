from flask import Blueprint

module_name = 'reports'
bp = Blueprint(module_name, __name__)


from src.routes.reports import index
from src.routes.reports import edit
from src.routes.reports import add
from src.routes.reports.view import view
from src.routes.reports.view import view_data