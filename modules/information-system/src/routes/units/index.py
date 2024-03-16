from . import bp, module_name

from flask import render_template
from src.models.user import User
from src.extensions.decorators import check_user_access
from flask_login import current_user
from flask_login import login_required
from src.models.module_roles import ModuleRole
from src.models.user_roles import UserRole

from src.controllers.unit import UnitController

@bp.route('/')
@check_user_access(module_name)
def index():
    controller = UnitController()
    items = controller.list_all()
    return render_template("admin/forms/view.html", 
                           modules=ModuleRole.get_available_modules(UserRole.get_active_role_ids(current_user.get_id())),
                           title=module_name.capitalize(), 
                           name=module_name, 
                           items=items)

