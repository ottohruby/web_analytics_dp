from . import bp, module_name

from flask_login import login_required
from flask_login import current_user
from src.models.module_roles import ModuleRole
from src.models.user_roles import UserRole

from flask import render_template, redirect, url_for, flash, jsonify, request
from src.models.user import User
from flask_login import login_required
from src.extensions.decorators import check_user_access
from src.models.event_stats import EventStat
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField,DateTimeField, BooleanField, FieldList, FormField 
from src.models.event_names import EventName
from src.models.agg_windows import AggWindow
from src.models.loggers import Logger
from src.models.dimensions import Dimension
from src.extensions.widgets import MultiCheckboxField
from datetime import datetime
from wtforms_components import TimeField
from src.models.metrics import Metric
from src.controllers.report import ReportController
from wtforms.validators import InputRequired
from src.models.allowed_event_metrics import AllowedEventMetric
from src.models.allowed_event_dimensions import AllowedEventDimension


def build_insert_form():
    available_metrics = Metric.get_all_active()
    available_allowed_metrics = AllowedEventMetric.get_all_allowed()
    available_metrics_dict = {metric['ID']: metric['Name'] for metric in available_metrics}
    for row in available_allowed_metrics[:]:
        name = available_metrics_dict.get(row['ID'])
        if name is not None:
            row["ID"] = str(row.get("ID")) + "||" + str(row.get("Name"))
            row['Name'] = str(name)
        else:
            available_allowed_metrics.remove(row)

    available_dims = Dimension.get_all_active()
    available_allowed_dims = AllowedEventDimension.get_all_allowed()
    available_dims_dict = {dim['ID']: dim['Name'] for dim in available_dims}
    for row in available_allowed_dims[:]:
        name = available_dims_dict.get(row['ID'])
        if name is not None:
            row["ID"] = str(row.get("ID")) + "||" + str(row.get("Name"))
            row['Name'] = str(name)
        else:
            available_allowed_dims.remove(row)

    class InsertForm(FlaskForm):
        name = StringField('Name', validators=[InputRequired()])
        description = StringField('Description')
        logger = SelectField('Logger')
        agg_window = SelectField('Granularity')
        timezone_choices = [(str(i), '+' + str(i)) if i > 0 else (str(i), str(i)) for i in range(-12, 15)]
        timezone = SelectField('Time Zone', choices=timezone_choices, default='0')
        time_selection = SelectField('Time Selection', choices=[('30m', 'Last 30 Minutes'), ('60m', 'Last 60 Minutes'), ('24h', 'Last 24 Hours'), ('48h', 'Last 48 Hours'), ('7d', 'Last 7 Days'), ('14d', 'Last 14 Days'), ('28d', 'Last 28 Days'), ('today', 'Today'), ('absolute', 'Fixed Range')])
        date_from = DateField('Date From', default=datetime.now())
        date_to = DateField('Date To', default=datetime.now())
        event = SelectField('Event')
        dimension = MultiCheckboxField('Dimensions')

        metric = SelectField('Metric')
        function = SelectField('Function', choices=[('1', 'SUM'), ('2', 'MIN'),('3', 'MAX')])
        sort = SelectField('Sort', choices=[('asc', 'ASC'), ('desc', 'DESC')])
        
        show_cumsum = SelectField('Chart - Show Cumulative Sum', choices=[ ('0', 'No'), ('1', 'Yes')])
        show_legend = SelectField('Chart - Show Legend', choices=[('1', 'Yes'), ('0', 'No')])
        # auto_refresh = SelectField('Auto Refresh', choices=[('0', 'No'), ('60', '60 s')])
        max_values = SelectField('Chart - Max Visible Lines', choices=[('5', '5'), ('10', '10')])

    form = InsertForm()
    form.event.choices = [(int(row["ID"]), row["Name"]) for row in EventName.get_all()]
    form.agg_window.choices = [(int(row["ID"]), row["Name"]) for row in AggWindow.get_all()]
    form.logger.choices = [(int(row["ID"]), row["Name"]) for row in Logger.get_with_state()]
    form.dimension.choices = [(str(item["ID"]), item['Name']) for item in available_allowed_dims]
    form.metric.choices = [((row["ID"]), row["Name"]) for row in available_allowed_metrics]
    return form
    

@bp.route('/add', methods=["GET", "POST"])
@check_user_access(module_name)
def add():
    form = build_insert_form()

    logged_user = current_user.get_id()

    if form.validate_on_submit():
        print("valid")
        try:
            
            report_data = {
                "logger": form.logger.data,
                "agg_window": form.agg_window.data,
                "timezone": form.timezone.data,
                "time_selection": form.time_selection.data,
                "date_from": form.date_from.data.strftime('%Y-%m-%d'),
                "date_to": form.date_to.data.strftime('%Y-%m-%d'),
                "event": form.event.data,
                "dimension": [item.split("||")[0] for item in form.dimension.data],
                "metric": form.metric.data.split("||")[0],
                "function": form.function.data,
                "sort": form.sort.data,
                "max_lines": int(form.max_values.data),
                "show_legend": form.show_legend.data,
                "show_cumsum": form.show_cumsum.data
            }

            controller = ReportController()
            controller.add(form.name.data, form.description.data, logged_user, report_data)
            flash('New item added successfully!', 'success')
        except Exception as e:
            print(e)
            flash(f'Error in adding details!', 'danger')

        return redirect(url_for(f'{module_name}.index'))
        

    return render_template("report/add.html", 
                           modules=ModuleRole.get_available_modules(UserRole.get_active_role_ids(logged_user)),
                           title='Create New Report', 
                           name=module_name, 
                           form=form)



