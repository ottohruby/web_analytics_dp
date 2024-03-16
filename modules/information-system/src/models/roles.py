from src.extensions.database import db
from sqlalchemy import Column, Integer, String, func, ForeignKey
from sqlalchemy.orm import relationship
from src.models.states import State
from enum import Enum
from src.models.model_base import ModelBase

class Role(db.Model, ModelBase):
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'analytics'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    state_id = db.Column(db.Integer, ForeignKey('analytics.states.id'))

    state = relationship("State", lazy='joined')

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