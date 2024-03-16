from . import bp, module_name

from flask_login import login_required
from flask_login import current_user
from src.extensions.decorators import check_user_access
from src.models.module_roles import ModuleRole
from src.models.user_roles import UserRole

from flask import Flask, render_template, redirect, url_for, flash
from src.controllers.event import EventController

@bp.route('/edit/<int:id>', methods=['GET','POST'])
@check_user_access(module_name)
def edit(id): 
    controller = EventController(id)
    form = controller.build_edit_form()    

    if form.validate_on_submit():
        try:
            controller.edit()
            flash('Settings updated successfully!', 'success')
        except Exception as e:
            print(e)
            flash(f'Error in updating settings!', 'danger')

        return redirect(url_for(f'{module_name}.index'))

    return render_template("forms/edit.html",
                           modules=ModuleRole.get_available_modules(UserRole.get_active_role_ids(current_user.get_id())),
                           title='Edit Event',
                           name=module_name, 
                           form=form,
                           id=id)
