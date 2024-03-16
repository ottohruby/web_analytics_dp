from src.extensions.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, event, func
from src.models.states import State
from sqlalchemy.orm import relationship, backref
from src.models.model_base import ModelBase
from src.models.user import User
from sqlalchemy.dialects.postgresql import JSON  # Import JSON type for PostgreSQL
import json
from src.models.agg_windows import AggWindow
from src.models.event_names import EventName

class Report(db.Model, ModelBase):
    __tablename__ = 'reports'
    __table_args__ = {'schema': 'analytics'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    state_id = db.Column(db.Integer, ForeignKey('analytics.states.id'))
    user_id = db.Column(db.Integer, ForeignKey('analytics.users.user_id'))
    data = Column(JSON)
    
    state = relationship("State", lazy='joined')
    user = relationship("User", lazy='joined')
    
    @classmethod
    def get_for_user(cls, user_id):                
        results = db.session.query(
                cls.id.label("ID"),
                cls.name.label("Name"),
                cls.data,
                cls.description.label("Description")
            ).filter(
                cls.user_id == user_id
            ).all()

        processed_results = [
            {
                "ID": row.ID,
                "Name": row.Name,
                "Event": EventName.get_name_by_id(row.data.get("event")),
                "Granularity": AggWindow.get_name_by_id(row.data.get("agg_window")),
                "Description": row.Description
            }
            for row in results
        ]

        return processed_results