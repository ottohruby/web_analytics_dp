from src.extensions.database import db
from sqlalchemy import Column, Integer, String
from dataclasses import dataclass

@dataclass
class AggWindow(db.Model):
    id: int
    name: String

    __tablename__ = 'agg_windows'
    __table_args__ = {'schema': 'analytics'}

    id = Column(Integer, primary_key=True)
    name = Column(String)