from src.extensions.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, func, case
from sqlalchemy.orm import relationship

from src.models.model_base import ModelBase

class Module(db.Model, ModelBase):
    __tablename__ = 'modules'
    __table_args__ = {'schema': 'analytics'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)

    state_id = db.Column(db.Integer, ForeignKey('analytics.states.id'))
    state = relationship("State", lazy='joined')

