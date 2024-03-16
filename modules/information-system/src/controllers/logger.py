from src.models.user import User
from src.models.loggers import Logger
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired

class LoggerController():
    def __init__(self, id=None):
        if id:
            self.model = Logger.query.get_or_404(id)

    def build_insert_form(self):
        class InsertForm(FlaskForm):
            name = StringField('Name', validators=[InputRequired()])
            description = StringField('Description', validators=[])

        self.form = InsertForm()
        return self.form
    
    def build_edit_form(self):
        class EditForm(FlaskForm):
            name = StringField('Name', validators=[InputRequired()])
            description = StringField('Description')
            state = SelectField('State')

            def get_state_name(self):
                return dict(self.state.choices).get(int(self.state.data))

        self.form = EditForm(obj=self.model)
        self.form.state.choices = self.model.get_available_states()
        
        return self.form
    
    def add(self):
        logger = Logger(name=self.form.name.data,
                          description=self.form.description.data)
        new_logger = Logger.add_with_state(logger, Logger.STATES.ACTIVE)   
        
        self.model = new_logger
        self.model.save()
        return new_logger
    
    def edit(self):       
        self.model.name = self.form.name.data
        self.model.description = self.form.description.data

        self.model.set_state(self.form.state.data, self.form.get_state_name())

        self.model.save()


    
