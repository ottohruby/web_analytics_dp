from flask import request, jsonify, render_template, redirect
from src.routes.dashboards import bp
from src.extensions.database import db
from src.models.loggers import Logger
from src.models.event_stats import EventStat
from src.models.event_names import EventName
from src.models.agg_windows import AggWindow
from sqlalchemy import func

@bp.route('/')
def admin_index():
    l = (EventStat
         .query
         .with_entities(
             func.DATE_TRUNC('minute', EventStat.insertion_ts).label('ts'), 
             EventStat.en_id,
             func.count().label('c'))
         .join(Logger)
         .join(EventName)
         .join(AggWindow)
         .filter(EventStat.aw_id == 0)
         .filter(EventStat.en_id <= 1)
         .group_by(func.DATE_TRUNC('minute', EventStat.insertion_ts), EventStat.en_id)
         ).all()
    serialized_items = [dict(row) for row in l]
    print(l)
    
    return jsonify(serialized_items)  #render_template('dashboards/index.html')

def admin_index2():
    l = (EventStat
         .query
         .with_entities(
             func.DATE_TRUNC('minute', EventStat.insertion_ts), 
             EventStat.en_id)
         .join(Logger)
         .join(EventName)
         .join(AggWindow)
         .filter(EventStat.aw_id == 0)
         .filter(EventStat.en_id <= 1)
         .group_by(func.DATE_TRUNC('minute', EventStat.insertion_ts), EventStat.en_id)
         .paginate(page=1, per_page=200)
         ).items
    serialized_items = [dict(row) for row in l]
    print(serialized_items)
    
    return jsonify(serialized_items)  #render_template('dashboards/index.html')