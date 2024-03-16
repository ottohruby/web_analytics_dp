from . import bp, module_name

from flask import render_template
from src.models.reports import Report
from src.extensions.decorators import check_user_access
from flask_login import current_user
from flask_login import login_required
from src.models.module_roles import ModuleRole
from src.models.user_roles import UserRole

@bp.route('/')
@check_user_access(module_name)
def index():
    user_id = current_user.get_id()
    return render_template("forms/view.html", 
                           modules=ModuleRole.get_available_modules(UserRole.get_active_role_ids(user_id)), 
                           title=module_name.capitalize(), 
                           name=module_name, 
                           items=Report.get_for_user(user_id),
                           form_with_view=1)

