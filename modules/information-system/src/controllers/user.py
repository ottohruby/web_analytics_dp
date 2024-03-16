from src.models.user import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from src.extensions.widgets import MultiCheckboxField
from wtforms.validators import InputRequired, Email
from werkzeug.security import generate_password_hash
from src.models.roles import Role
from src.models.user_roles import UserRole
from werkzeug.security import check_password_hash
from flask_login import login_user

class UserControllerException(Exception):
    pass

class UserController():
    def __init__(self, id=None):
        if id:
            self.model = User.query.get_or_404(id)
    
    def login(self, name, password):
        user = User.query.filter_by(name=name).first()
        if user:
            if check_password_hash(user.password_hash, password):
                login_user(user)
            else:
                raise UserControllerException("Invalid username or password!")
        else:
            raise UserControllerException('Invalid username or password', 'danger')
        return user


    def build_insert_form(self):
        available_roles = Role.get_all_active()
        class InsertForm(FlaskForm):
            name = StringField('Username', validators=[InputRequired()])
            email = StringField('Email', validators=[InputRequired()])
            password = PasswordField('Password', validators=[InputRequired()])
            roles = MultiCheckboxField("Roles")

        self.form = InsertForm()
        self.form.roles.choices = [(str(role["ID"]), role['Name']) for role in available_roles]
        return self.form
    
    def build_edit_form(self):
        available_roles = self.model.get_all_available_roles()
        default_roles = [str(role['ID']) for role in available_roles if role["state"] == "GRANTED"]
        class EditForm(FlaskForm):
            name = StringField('Username', validators=[InputRequired()])
            email = StringField('Email', validators=[InputRequired()])
            password = PasswordField('Password', validators=[])
            state = SelectField('State')
            roles = MultiCheckboxField("Roles", default=default_roles)

            def get_state_name(self):
                return dict(self.state.choices).get(int(self.state.data))

        self.form = EditForm(obj=self.model)
        self.form.state.choices = self.model.get_available_states()
        self.form.roles.choices = [(str(role["ID"]), role['Name']) for role in available_roles]
        
        return self.form
    
    def add(self):
        user = User(name=self.form.name.data,
                          email=self.form.email.data,
                          password_hash = generate_password_hash(self.form.password.data))
        new_user = User.add_with_state(user, User.STATES.ACTIVE)   

        for role in self.form.roles.choices:
            state = UserRole.STATES.GRANTED if str(role[0]) in self.form.roles.data else UserRole.STATES.DENY
            role = UserRole(role_id=int(role[0]), user_id=new_user.user_id)
            UserRole.add_with_state(role, state)
        
        self.model = new_user
        self.model.save()
        return new_user
    
    def edit(self):
        if not self.model.state:
            raise UserControllerException("User has no state!")
        
        self.model.name = self.form.name.data
        self.model.email = self.form.email.data

        if self.form.password.data:
            self.model.password_hash = generate_password_hash(self.form.password.data)

        self.model.set_state(self.form.state.data, self.form.get_state_name())
        for role in self.model.user_role:
            permission = UserRole.STATES.DENY
            if(str(role.role_id) in self.form.roles.data):
                permission = UserRole.STATES.GRANTED
            role.set_state(permission.value, permission.name)

        self.model.save()


    
