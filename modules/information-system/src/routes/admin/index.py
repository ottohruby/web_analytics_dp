from . import bp
from flask import request, jsonify, render_template, redirect
from src.extensions.database import db
from src.models.loggers import Logger
from src.models.event_stats import EventStat
from src.models.event_names import EventName
from src.models.agg_windows import AggWindow
from sqlalchemy import func

@bp.route('/')
def index():
    return render_template('admin/index.html', title="Homepage")

