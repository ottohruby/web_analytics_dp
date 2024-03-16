from src.extensions.database import db

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.models.states import State
from src.models.model_base import ModelBase
from src.models.units import Unit
class Metric(db.Model, ModelBase):
    __tablename__ = 'metrics'
    __table_args__ = {'schema': 'analytics'}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    base_unit_id = db.Column(db.Integer, ForeignKey('analytics.units.id'))

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
    def get_names(cls, ids, function_id):
        fn = ''
        if int(function_id) == 1:
            fn = 'SUM'
        elif int(function_id) == 2:
            fn = 'Min'
        elif int(function_id) == 3:
            fn = 'Max'

        query_result = db.session.query(
            cls.name,
            Unit.name
        ).filter(
            cls.id.in_(ids)
        ).join(
            Unit, Unit.id==cls.base_unit_id
        ).order_by(cls.id).all()
        names = [f"{row[0]}[{row[1]}] ({fn})" for row in query_result]

        return names