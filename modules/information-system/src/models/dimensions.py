from src.extensions.database import db
from sqlalchemy import Column, Integer, String
from dataclasses import dataclass

@dataclass
class Dimension(db.Model):
    id: int
    name: str
    description: str
    
    __tablename__ = 'dimensions'
    __table_args__ = {'schema': 'analytics'}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
