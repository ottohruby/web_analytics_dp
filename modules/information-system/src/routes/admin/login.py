from . import bp

from flask import Flask, render_template, redirect, url_for, flash, jsonify
from src.models.user import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.security import check_password_hash
from src.controllers.user import UserController
from src.extensions.decorators import check_user_access
from flask_login import current_user
from flask_login import login_required
from src.models.module_roles import ModuleRole
from src.models.user_roles import UserRole

class LoginForm(FlaskForm):
    name = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data

        controller = UserController()
        try:
            controller.login(name, password)
            flash('Logged in successfully!', 'success')
            return redirect(url_for(f'index'))
        except Exception as e:
            flash(e, 'danger')
            flash('Invalid username or password', 'danger')

    return render_template('admin/login.html',
                           modules=ModuleRole.get_available_modules(UserRole.get_active_role_ids(current_user.get_id())),
                           form=form)

