from src.extensions.database import db

from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from dataclasses import dataclass

@dataclass
class Logger(db.Model):
    id: int
    name: str
    description: str
    
    __tablename__ = 'loggers'
    __table_args__ = {'schema': 'analytics'}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

