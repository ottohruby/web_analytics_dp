from . import bp, module_name

from flask_login import login_required
from flask_login import current_user
from src.extensions.decorators import check_user_access
from src.models.module_roles import ModuleRole
from src.models.user_roles import UserRole

from flask import Flask, render_template, redirect, url_for, flash, jsonify
from src.controllers.dimension import DimensionController

@bp.route("add", methods=["GET", "POST"])
@check_user_access(module_name)
def add():
    controller = DimensionController()
    form = controller.build_insert_form()

    if form.validate_on_submit():
        try:
            controller.add()
            flash('New item added successfully!', 'success')
        except Exception as e:
            print(e)
            flash(f'Error in adding details!', 'danger')

        return redirect(url_for(f'{module_name}.index'))

    return render_template("forms/add.html", 
                           modules=ModuleRole.get_available_modules(UserRole.get_active_role_ids(current_user.get_id())),
                           title='Create New Dimension', 
                           name=module_name, 
                           form=form)
