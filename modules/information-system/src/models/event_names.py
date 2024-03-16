from src.extensions.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, event, func
from src.models.states import State
from sqlalchemy.orm import relationship, backref
from enum import Enum
from sqlalchemy.orm import joinedload, contains_eager
from src.models.model_base import ModelBase
from src.models.allowed_event_dimensions import AllowedEventDimension
from src.models.allowed_event_metrics import AllowedEventMetric
from src.models.dimensions import Dimension
from src.models.metrics import Metric


class EventName(db.Model, ModelBase):
    __tablename__ = 'event_names'
    __table_args__ = {'schema': 'analytics'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    state_id = db.Column(db.Integer, ForeignKey('analytics.states.id'))
    
    state = relationship("State", lazy='joined')
    allowed_event_dimension = relationship("AllowedEventDimension", lazy='joined')
    allowed_event_metric = relationship("AllowedEventMetric", lazy='joined')

    @classmethod
    def get_all(cls):
        results = db.session.query(
                cls.id.label("ID"),
                cls.name.label("Name")
            ).join(
                State, isouter=True
            ).all()

        return results
    
    @classmethod
    def get_with_state(cls):
        results = db.session.query(
                cls.id.label("ID"),
                cls.name.label("Name"),
                cls.description.label("Description"),
                State.state_name.label("State")
            ).join(
                State, State.id == cls.state_id, isouter=True
            ).filter(
                State.state_name != cls.STATES.DELETED.name
            ).all()

        return [dict(row) for row in results]
    
    def get_all_available_dims(self):
        results = db.session.query(
            AllowedEventDimension.event_id,
            State.state_name.label("state"),
            Dimension.name.label("Name"),
            Dimension.id.label("ID")
        ).join(
            State, State.id == AllowedEventDimension.state_id and State.state_name== self.STATES.ACTIVE.name
        ).join(
            Dimension, Dimension.id == AllowedEventDimension.dimension_id
        ).filter(
            AllowedEventDimension.event_id == self.id
        ).all()
        
        return [dict(row) for row in results]
    
    def get_all_available_metrics(self):
        results = db.session.query(
            AllowedEventMetric.event_id,
            State.state_name.label("state"),
            Metric.name.label("Name"),
            Metric.id.label("ID")
        ).join(
            State, State.id == AllowedEventMetric.state_id and State.state_name== self.STATES.ACTIVE.name
        ).join(
            Metric, Metric.id == AllowedEventMetric.metric_id
        ).filter(
            AllowedEventMetric.event_id == self.id
        ).all()
        
        return [dict(row) for row in results]

    @classmethod
    def get_name_by_id(cls, id):
        result = db.session.query(
                cls.name
            ).filter(
                cls.id == id
            ).scalar()

        return result
