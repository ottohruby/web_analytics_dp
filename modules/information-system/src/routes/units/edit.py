from . import bp, module_name

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import login_required
from flask_login import current_user
from src.extensions.decorators import check_user_access
from src.controllers.unit import UnitController
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired
from src.models.module_roles import ModuleRole
from src.models.user_roles import UserRole
from src.models.units import Unit

def build_edit_form(model):
    available_units = Unit.get_base_units()
    selected_unit = None

    for unit_tuple in available_units:
        print(unit_tuple, model.base_unit_id, model.id)
        if model.base_unit_id is None:
            selected_unit = (None, '')
        print(selected_unit)

    class EditForm(FlaskForm):
        name = StringField('Name', validators=[InputRequired()])
        description = StringField('Description')
        amount = StringField('Rate', validators=[InputRequired()])
        base_unit_id = SelectField('Parent Unit', default=selected_unit)
        state = SelectField('State')

        def get_state_name(self):
            return dict(self.state.choices).get(int(self.state.data))

    children = Unit.children_count(model.id)
    if children < 1:
        form = EditForm(obj=model)
        form.base_unit_id.choices = [(None, '')] + [(str(item["ID"]), item['Name']) for item in available_units]
    else:
        class EditFormText(EditForm):
            text = StringField('Label', default=f'This Unit has {children} {"children" if children > 1 else "child"}!', render_kw={'readonly': True})
        form = EditFormText(obj=model)
        form.base_unit_id.choices = [(None, '')]

    form.state.choices = model.get_available_states()
    return form

@bp.route('/edit/<int:id>', methods=['GET','POST'])
@check_user_access(module_name)
def edit(id): 
    controller = UnitController(id)
    form = build_edit_form(controller.model)    

    if form.validate_on_submit():
        try:
                
            controller.edit(form.name.data,
                            form.amount.data,
                            form.description.data,
                            form.state.data,
                            form.get_state_name(),
                            form.base_unit_id.data)
            flash('Settings updated successfully!', 'success')
        except Exception as e:
            print(e)
            flash(f'Error in updating settings!', 'danger')

        return redirect(url_for(f'{module_name}.index'))

    return render_template("forms/edit.html",
                           modules=ModuleRole.get_available_modules(UserRole.get_active_role_ids(current_user.get_id())),
                           title='Edit Units',
                           name=module_name, 
                           form=form,
                           id=id)
