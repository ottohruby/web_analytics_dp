from src.extensions.database import db

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.models.states import State
from src.models.model_base import ModelBase

class Logger(db.Model, ModelBase):
    __tablename__ = 'loggers'
    __table_args__ = {'schema': 'analytics'}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    state_id = db.Column(db.Integer, ForeignKey('analytics.states.id'))
    state = relationship("State", lazy='joined')

    
    @classmethod
    def get_with_state(cls):
        results = db.session.query(
                cls.id.label("ID"),
                cls.name.label("Name"),
                cls.description.label("Description"),
                State.state_name.label("State")
            ).join(
                State, isouter=True
            ).all()
        
        return [dict(row) for row in results]