from flask import request, jsonify, render_template, redirect
from src.routes.admin import bp
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from src.extensions.database import db
from src.models.loggers import Logger
from src.models.event_stats import EventStat
from src.models.event_names import EventName
from src.models.agg_windows import AggWindow

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    role = StringField('role', validators=[DataRequired()])

@bp.route('/')
def admin_index():
    # l = Logger.query.all()
    # print(l)
    # l = EventStat.query.all()
    # print(l)
        # https://stackoverflow.com/questions/27900018/flask-sqlalchemy-query-join-relational-tables

    l = (EventStat
         .query
         .join(Logger)
         .join(EventName)
         .join(AggWindow)
         .paginate(page=1, per_page=200)
         )
    print(l)
    
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('admin/index.html', form=form)