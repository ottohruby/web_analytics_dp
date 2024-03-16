from src.models.event_names import EventName
from src.models.dimensions import Dimension
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired
from src.extensions.widgets import MultiCheckboxField
from src.models.allowed_event_dimensions import AllowedEventDimension
from src.models.allowed_event_metrics import AllowedEventMetric
from src.models.metrics import Metric

class EventController():
    def __init__(self, id=None):
        if id:
            self.model = EventName.query.get_or_404(id)

    def build_insert_form(self):
        available_dims = Dimension.get_all_active()
        available_metrics = Metric.get_all_active()
        class InsertForm(FlaskForm):
            name = StringField('Name', validators=[InputRequired()])
            description = StringField('Description')
            dims = MultiCheckboxField("Dimensions")
            metrics = MultiCheckboxField("Metrics")

        self.form = InsertForm()
        self.form.dims.choices = [(str(item["ID"]), item['Name']) for item in available_dims]
        self.form.metrics.choices = [(str(item["ID"]), item['Name']) for item in available_metrics]
        return self.form
    
    def build_edit_form(self):
        available_dims = self.model.get_all_available_dims()
        default_dims = [str(item['ID']) for item in available_dims if item["state"] == "ALLOWED"]

        available_metrics = self.model.get_all_available_metrics()
        default_metrics = [str(item['ID']) for item in available_metrics if item["state"] == "ALLOWED"]
        class EditForm(FlaskForm):
            name = StringField('Name', validators=[InputRequired()])
            description = StringField('Description')
            state = SelectField('State')
            dims = MultiCheckboxField("Dimensions", default=default_dims)
            metrics = MultiCheckboxField("Metrics", default=default_metrics)

            def get_state_name(self):
                return dict(self.state.choices).get(int(self.state.data))

        self.form = EditForm(obj=self.model)
        self.form.state.choices = self.model.get_available_states()
        self.form.dims.choices = [(str(role["ID"]), role['Name']) for role in available_dims]
        self.form.metrics.choices = [(str(role["ID"]), role['Name']) for role in available_metrics]
        
        return self.form
    
    def add(self):
        event = EventName(name=self.form.name.data,
                          description=self.form.description.data)
        new_event = EventName.add_with_state(event, EventName.STATES.ACTIVE)  

        for item in self.form.dims.choices:
            state = AllowedEventDimension.STATES.ALLOWED if str(item[0]) in self.form.dims.data else AllowedEventDimension.STATES.DISABLED
            dim = AllowedEventDimension(dimension_id=int(item[0]), event_id=new_event.id)
            AllowedEventDimension.add_with_state(dim, state)
        
        for item in self.form.metrics.choices:
            state = AllowedEventMetric.STATES.ALLOWED if str(item[0]) in self.form.metrics.data else AllowedEventMetric.STATES.DISABLED
            metric = AllowedEventMetric(metric_id=int(item[0]), event_id=new_event.id)
            AllowedEventMetric.add_with_state(metric, state)
        
        self.model = new_event
        self.model.save()
        return new_event
    
    def edit(self):       
        self.model.name = self.form.name.data
        self.model.description = self.form.description.data

        self.model.set_state(self.form.state.data, self.form.get_state_name())
        for item in self.model.allowed_event_dimension:
            permission = AllowedEventDimension.STATES.DISABLED
            if(str(item.dimension_id) in self.form.dims.data):
                permission = AllowedEventDimension.STATES.ALLOWED
            item.set_state(permission.value, permission.name)

        for item in self.model.allowed_event_metric:
            permission = AllowedEventMetric.STATES.DISABLED
            if(str(item.metric_id) in self.form.metrics.data):
                permission = AllowedEventMetric.STATES.ALLOWED
            item.set_state(permission.value, permission.name)

        self.model.save()


    
