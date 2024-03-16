from src.extensions.database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from src.models.states import State
from enum import Enum 
from src.models.model_base import ModelBase

class StateEnum(Enum):
    ALLOWED = 1
    DISABLED = 2

class AllowedEventDimension(db.Model, ModelBase):
    __tablename__ = 'allowed_event_dimensions'
    __table_args__ = {'schema': 'analytics'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, ForeignKey('analytics.event_names.id'))
    dimension_id = db.Column(db.Integer, ForeignKey('analytics.dimensions.id'))

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
            cls.dimension_id.label("ID"),
            cls.event_id.label("Name")
            ).join(
                State, isouter=True
            ).filter(
                State.state_name == cls.STATES.ALLOWED.name
            ).all()
        
        return [dict(row) for row in results]