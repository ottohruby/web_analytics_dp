from src.extensions.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, event, func
from dataclasses import dataclass
from src.models.states import State
from sqlalchemy.orm import relationship, backref
from enum import Enum
from src.models.states import State
from src.models.model_base import ModelBase

class StateEnum(Enum):
    ACTIVE = 1
    INACTIVE = 2
    DELETED = 3

class Dimension(db.Model, ModelBase):
    __tablename__ = 'dimensions'
    __table_args__ = {'schema': 'analytics'}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    state_id = db.Column(db.Integer, ForeignKey('analytics.states.id'))
    state = relationship("State", lazy='joined')

    STATES = StateEnum

    STATE_TRANSITIONS = {
        STATES.ACTIVE.value: [STATES.INACTIVE, STATES.DELETED],
        STATES.INACTIVE.value: [STATES.ACTIVE, STATES.DELETED],
        STATES.DELETED.value: [STATES.DELETED]
    }

    def get_available_states(self):
        transitions = []
        if self.state:
            transitions = [(state.value, state.name) for state in self.STATE_TRANSITIONS[self.state.state_number]]
        return transitions

    @classmethod
    def get_with_state(cls):
        results = db.session.query(
                cls.id.label("ID"),
                cls.name.label("Name"),
                cls.description.label("Description"),
                State.state_name.label("State"),
                func.concat(func.cast(State.changed_ts, db.String(10)), " ").label("Last Change")
            ).join(
                State, isouter=True
            ).all()

        return [dict(row) for row in results]
    
    @classmethod
    def get_all_active(cls):
        results = db.session.query(
                cls.id.label("ID"),
                cls.name.label("Name")
            ).join(
                State, isouter=True
            ).filter(
                State.state_name == cls.STATES.ACTIVE.name
            ).all()
        
        return [dict(row) for row in results]
    
    @classmethod
    def get_names(cls, ids):
        query_result = db.session.query(
            cls.name,
        ).filter(
            cls.id.in_(ids)
        ).order_by(cls.id).all()
        names = [row[0] for row in query_result]

        return names
    
