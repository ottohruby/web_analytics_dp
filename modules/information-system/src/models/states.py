from src.extensions.database import db
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

class State(db.Model):
    __tablename__ = 'states'
    __table_args__ = {'schema': 'analytics'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    state_number = Column(Integer, nullable=False)
    state_name = Column(String)
    changed_ts = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

