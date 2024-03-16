from . import bp, module_name

from flask_login import login_required
from flask_login import current_user
from src.extensions.decorators import check_user_access
from src.models.module_roles import ModuleRole
from src.models.user_roles import UserRole
from src.models.units import Unit
from flask import Flask, render_template, redirect, url_for, flash, jsonify
from src.controllers.unit import UnitController
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired

def build_insert_form(base_units):
    available_units = Unit.get_base_units()
    class InsertForm(FlaskForm):
        name = StringField('Name', validators=[InputRequired()])
        description = StringField('Description', validators=[])
        amount = StringField('Rate', default='1', validators=[InputRequired()])
        base_unit_id = SelectField('Parent Unit')
        
    form = InsertForm()
    form.base_unit_id.choices = [(None, '')] + [(str(item["ID"]), item['Name']) for item in available_units]

    return form

@bp.route("add", methods=["GET", "POST"])
@check_user_access(module_name)
def add():
    controller = UnitController()
    form = build_insert_form(controller.list_only_base())

    if form.validate_on_submit():
        try:
            controller.add(form.name.data, 
                           form.description.data, 
                           form.amount.data, 
                           form.base_unit_id.data)
            
            flash('New item added successfully!', 'success')
        except Exception as e:
            flash(f'Error in adding details!', 'danger')

        return redirect(url_for(f'{module_name}.index'))

    return render_template("forms/add.html", 
                           modules=ModuleRole.get_available_modules(UserRole.get_active_role_ids(current_user.get_id())),
                           title='Create New Unit', 
                           name=module_name, 
                           form=form)
