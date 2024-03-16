from src.extensions.database import db

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from src.models.states import State
from src.models.model_base import ModelBase
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import case
from sqlalchemy import func

class Unit(db.Model, ModelBase):
    __tablename__ = 'units'
    __table_args__ = {'schema': 'analytics'}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    is_base = Column(Integer)
    amount = Column(Numeric, nullable=False)

    base_unit_id = db.Column(db.Integer, ForeignKey('analytics.units.id'))
    base_unit = relationship("Unit")

    state_id = db.Column(db.Integer, ForeignKey('analytics.states.id'))
    state = relationship("State", lazy='joined')

    @classmethod
    def get_with_state(cls):
        unit_alias = aliased(Unit, name="Unit_Base")

        results = db.session.query(
                cls.id.label("ID"),
                cls.name.label("Name"),
                case([(unit_alias.name.isnot(None), unit_alias.name)], else_='Yes').label("Base Unit"),
                cls.amount.label("Rate"),
                cls.description.label("Description"),
                State.state_name.label("State")
            ).select_from(
                cls
            ).join(
                State, isouter=True
            ).join(
                unit_alias, cls.base_unit_id==unit_alias.id, isouter=True
            ).all()
        
        return [dict(row) for row in results]
    
    @classmethod
    def get_base_units(cls):
        results = db.session.query(
            cls.id.label("ID"),
            cls.name.label("Name")
        ).join(
            State, State.id == cls.state_id
        ).filter(
            cls.base_unit_id == None
        ).all()
        
        return [dict(row) for row in results]
    
    @classmethod
    def children_count(cls, id):
        return db.session.query(
            func.count(cls.id)).filter(cls.base_unit_id == id).scalar()