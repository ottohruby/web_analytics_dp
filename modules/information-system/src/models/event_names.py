from src.extensions.database import db
from sqlalchemy import Column, Integer, String
from dataclasses import dataclass

@dataclass
class EventName(db.Model):
    id: int
    name: str
    description: str
    
    __tablename__ = 'event_names'
    __table_args__ = {'schema': 'analytics'}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
