from src.extensions.database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from src.models.states import State
from enum import Enum 
from src.models.model_base import ModelBase

class StateEnum(Enum):
    GRANTED = 1
    DENY = 2

class UserRole(db.Model, ModelBase):
    __tablename__ = 'user_roles'
    __table_args__ = {'schema': 'analytics'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, ForeignKey('analytics.roles.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, ForeignKey('analytics.users.user_id', ondelete='CASCADE'))

    state_id = db.Column(db.Integer, ForeignKey('analytics.states.id'))
    state = relationship("State", lazy='joined')

    STATES = StateEnum

    STATE_TRANSITIONS = {
        STATES.GRANTED.value: [STATES.GRANTED, STATES.DENY],
        STATES.DENY.value: [STATES.DENY, STATES.GRANTED]
    }

    @classmethod
    def get_active_role_ids(cls, user_id):
        results = db.session.query(
            cls.role_id.label("id"),
        ).join(
            State, State.id==cls.state_id
        ).filter(
            cls.user_id == user_id,
            State.state_name == cls.STATES.GRANTED.name
        ).all()

        return [dict(row).get("id") for row in results]