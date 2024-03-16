from src.models.metrics import Metric
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired
from src.models.allowed_event_metrics import AllowedEventMetric
from src.models.event_names import EventName
from src.models.units import Unit

class MetricController():
    def __init__(self, id=None):
        if id:
            self.model = Metric.query.get_or_404(id)

    def build_insert_form(self):
        available_units = Unit.get_base_units()
        class InsertForm(FlaskForm):
            name = StringField('Name', validators=[InputRequired()])
            description = StringField('Description', validators=[])
            base_unit_id = SelectField("Base Unit")

        self.form = InsertForm()
        self.form.base_unit_id.choices = [(str(item["ID"]), item['Name']) for item in available_units]
        return self.form
    
    def build_edit_form(self):
        available_units = Unit.get_base_units()
        selected_unit = None

        for unit_tuple in available_units:
            if unit_tuple["ID"] == self.model.base_unit_id:
                selected_unit = unit_tuple
                break

        class EditForm(FlaskForm):
            name = StringField('Name', validators=[InputRequired()])
            description = StringField('Description')
            state = SelectField('State')
            base_unit_id = SelectField("Base Unit", default=selected_unit)

            def get_state_name(self):
                return dict(self.state.choices).get(int(self.state.data))

        self.form = EditForm(obj=self.model)
        self.form.state.choices = self.model.get_available_states()
        self.form.base_unit_id.choices = [(str(item["ID"]), item['Name']) for item in available_units]
        
        return self.form
    
    def add(self):
        row = Metric(name=self.form.name.data,
                          description=self.form.description.data,
                          base_unit_id=self.form.base_unit_id.data)
        new_row = Metric.add_with_state(row, Metric.STATES.ACTIVE)   

        for item in EventName.get_all():
            allowed = AllowedEventMetric(event_id=item[0], metric_id=new_row.id)
            state = AllowedEventMetric.STATES.DISABLED
            AllowedEventMetric.add_with_state(allowed, state)
        
        self.model = new_row
        self.model.save()
        return new_row
    
    def edit(self):       
        self.model.name = self.form.name.data
        self.model.description = self.form.description.data
        self.model.base_unit_id = self.form.base_unit_id.data

        self.model.set_state(self.form.state.data, self.form.get_state_name())

        self.model.save()


    
