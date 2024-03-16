from src.models.dimensions import Dimension
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired
from src.models.allowed_event_dimensions import AllowedEventDimension
from src.models.event_names import EventName

class DimensionController():
    def __init__(self, id=None):
        if id:
            self.model = Dimension.query.get_or_404(id)

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
        dim = Dimension(name=self.form.name.data,
                          description=self.form.description.data)
        new_dim = Dimension.add_with_state(dim, Dimension.STATES.ACTIVE)   

        for item in EventName.get_all():
            print(item, new_dim, new_dim.id)
            allowed = AllowedEventDimension(event_id=item[0], dimension_id=new_dim.id)
            state = AllowedEventDimension.STATES.DISABLED
            AllowedEventDimension.add_with_state(allowed, state)
        
        self.model = new_dim
        self.model.save()
        return new_dim
    
    def edit(self):       
        self.model.name = self.form.name.data
        self.model.description = self.form.description.data

        self.model.set_state(self.form.state.data, self.form.get_state_name())

        self.model.save()


    
