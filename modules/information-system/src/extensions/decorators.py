from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for
from src.models.module_roles import ModuleRole
from functools import wraps
from src.models.user_roles import UserRole

def check_user_access(module_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if type(current_user.is_active)==bool:
                flash("User is not logged in!", "warning")
                return redirect(url_for('admin.login'))      
            if not current_user.is_active():
                flash("User is not active", "warning")
                return redirect(url_for('admin.login'))
            print(current_user.user_role[0].role_id)
            required_roles = ModuleRole.get_required_role_ids(module_name)
            user_roles = UserRole.get_active_role_ids(current_user.get_id())
            if not all(req_role in user_roles for req_role in required_roles):
                flash("User has no permission to access this module!", "warning")
                return redirect(url_for('index'))
            
            #check if user has required role id
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator