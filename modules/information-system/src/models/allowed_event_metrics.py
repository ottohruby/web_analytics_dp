from src.extensions.database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from src.models.states import State
from enum import Enum 
from src.models.model_base import ModelBase
from src.models.metrics import Metric
from sqlalchemy.orm import aliased
from sqlalchemy import func, select

class StateEnum(Enum):
    ALLOWED = 1
    DISABLED = 2

class AllowedEventMetric(db.Model, ModelBase):
    __tablename__ = 'allowed_event_metrics'
    __table_args__ = {'schema': 'analytics'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, ForeignKey('analytics.event_names.id'))
    metric_id = db.Column(db.Integer, ForeignKey('analytics.metrics.id'))

    state_id = db.Column(db.Integer, ForeignKey('analytics.states.id'))
    state = relationship("State", lazy='joined')

    STATES = StateEnum

    STATE_TRANSITIONS = {
        STATES.ALLOWED.value: [STATES.ALLOWED, STATES.DISABLED],
        STATES.DISABLED.value: [STATES.DISABLED, STATES.ALLOWED],
    }

    @classmethod
    def get_all_allowed(cls):
        results = db.session.query(
            cls.metric_id.label("ID"),
            cls.event_id.label("Name")
            ).join(
                State, isouter=True
            ).filter(
                State.state_name == cls.STATES.ALLOWED.name
            ).all()
        
        return [dict(row) for row in results]
