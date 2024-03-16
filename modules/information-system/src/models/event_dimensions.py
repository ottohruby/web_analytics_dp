from src.extensions.database import db
from sqlalchemy import Column, Integer, String, ForeignKey

class EventDimension(db.Model):
    __tablename__ = 'event_dimensions'
    __table_args__ = {'schema': 'analytics'}

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('analytics.event_stats.event_id'))
    dim_id = Column(Integer, ForeignKey('analytics.dimensions.id'))
    value = Column(String)



