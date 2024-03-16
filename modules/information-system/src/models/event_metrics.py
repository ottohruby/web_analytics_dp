from src.extensions.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric

class EventMetric(db.Model):
    __tablename__ = 'event_metrics'
    __table_args__ = {'schema': 'analytics'}

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('analytics.event_stats.event_id'))
    metric_id  = Column(Integer, ForeignKey('analytics.metrics.id'))
    unit_id  = Column(Integer, ForeignKey('analytics.units.id'))
    value = Column(Numeric)



