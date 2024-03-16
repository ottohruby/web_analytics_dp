from . import bp, module_name

from flask import Flask, render_template, redirect, url_for, flash, jsonify
from src.models.user import User

from src.controllers.user import UserController

from flask_login import current_user
from flask_login import login_required
from src.extensions.decorators import check_user_access
from src.models.module_roles import ModuleRole
from src.models.user_roles import UserRole

@bp.route("add", methods=["GET", "POST"])
@check_user_access(module_name)
def add():
    controller = UserController()
    form = controller.build_insert_form()

    if form.validate_on_submit():
        try:
            controller.add()
            flash('New item added successfully!', 'success')
        except Exception as e:
            flash(f'Error in adding details!', 'danger')

        return redirect(url_for(f'{module_name}.index'))

    return render_template("forms/add.html", 
                           modules=ModuleRole.get_available_modules(UserRole.get_active_role_ids(current_user.get_id())),
                           title='Create New User', 
                           name=module_name, 
                           form=form)
