from . import bp, module_name

from flask import render_template, jsonify, request
from src.models.user import User
from flask_login import login_required
from src.extensions.decorators import check_user_access
from src.models.event_stats import EventStat
from flask_login import current_user
from src.controllers.report import ReportController
import json
import datetime
from src.models.module_roles import ModuleRole
from src.models.user_roles import UserRole  
from src.models.dimensions import Dimension
from src.models.metrics import Metric
from src.controllers.event import EventController

@bp.route('/view/<int:id>', methods=["GET"])
@check_user_access(module_name)
def view(id):
    user_id = current_user.get_id()
    controller = ReportController(id)
    
    dims = Dimension.get_names(controller.model.data.get("dimension", []))
    metrics = Metric.get_names([controller.model.data.get("metric")], controller.model.data.get("function"))
    return render_template("report/view.html", 
                           title=controller.model.name,
                           description = controller.model.description,
                           modules=ModuleRole.get_available_modules(UserRole.get_active_role_ids(user_id)), 
                           headers=dims + metrics,
                           yaxis_title=metrics[0],
                           id=str(id),
                           event_name=EventController(controller.model.data.get("event")).model.name)

@bp.route('/view/<int:id>/data', methods=["POST"])
@check_user_access(module_name)
def view_data(id):
    logged_user = current_user.get_id()
    controller = ReportController(id)
    report_settings = controller.model.data
    
    form_data = request.get_json()

    timezone_offset_hours = report_settings.get("timezone", 0)
    ts = report_settings.get("time_selection", 'absolute')
    if ts == "absolute":
        start_date = datetime.datetime.strptime(report_settings["date_from"], '%Y-%m-%d')
        end_date = datetime.datetime.strptime(report_settings["date_to"], '%Y-%m-%d')
    else:
        if ts == 'today':
            start_date = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = datetime.datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999)
        elif ts == '30m':
            start_date = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
            end_date = datetime.datetime.utcnow()
        elif ts == '24h':
            start_date = datetime.datetime.utcnow() - datetime.timedelta(days=1)
            end_date = datetime.datetime.utcnow()
        elif ts == '48h':
            start_date = datetime.datetime.utcnow() - datetime.timedelta(days=2)
            end_date = datetime.datetime.utcnow()
        elif ts == '7d':
            start_date = datetime.datetime.utcnow() - datetime.timedelta(days=7)
            end_date = datetime.datetime.utcnow()
        elif ts == '14d':
            start_date = datetime.datetime.utcnow() - datetime.timedelta(days=14)
            end_date = datetime.datetime.utcnow()
        elif ts == '28d':
            start_date = datetime.datetime.utcnow() - datetime.timedelta(days=28)
            end_date = datetime.datetime.utcnow()
    
    start_date.replace(second=0, microsecond=0)
    end_date.replace(second=0, microsecond=0)
    start_datetime = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_datetime = end_date.strftime('%Y-%m-%d %H:%M:%S')

    data = EventStat.stats(
        report_settings.get("logger", 1),
        report_settings.get("agg_window", 2),
        int(timezone_offset_hours),
        start_datetime,
        end_datetime,
        report_settings.get("event", 1),
        [int(i) for i in report_settings.get("dimension", [1])],
        [int(report_settings.get("metric", 1))],
        [int(report_settings.get("function", 1))],
        report_settings.get("sort", 'asc'),
        form_data,
        int(report_settings.get("max_lines", 5)),
        True if report_settings.get("show_legend", '1') == '1' else False,
        True if report_settings.get("show_cumsum", '0') == '1' else False
    )
    return jsonify(data)