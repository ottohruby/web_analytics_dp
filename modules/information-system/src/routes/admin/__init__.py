from flask import Blueprint

bp = Blueprint('admin', __name__)

from src.routes.admin.index import index
from src.routes.admin.login import login
from src.routes.admin.logout import logout
# from src.routes.admin.user.users import users
# from src.routes.admin.user.edit_user import edit_user
# from src.routes.admin.user.add_user import add_user