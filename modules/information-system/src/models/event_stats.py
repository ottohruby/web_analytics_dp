from src.extensions.database import db
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from dataclasses import dataclass
import datetime

@dataclass
class EventStat(db.Model):
    event_id: int
    lg_id: int
    en_id: int
    ev_ts: datetime.datetime
    insertion_ts: datetime.datetime
    aw_id: int
    is_processed: int
    
    __tablename__ = 'event_stats'
    __table_args__ = {'schema': 'analytics'}

    event_id = Column(Integer, primary_key=True)
    lg_id = Column(Integer, ForeignKey('analytics.loggers.id'))
    en_id = Column(Integer, ForeignKey('analytics.event_names.id'))
    ev_ts = Column(TIMESTAMP(timezone=True), nullable=False)
    insertion_ts = Column(TIMESTAMP(timezone=True), server_default='now()', nullable=False)
    aw_id = Column(Integer, ForeignKey('analytics.agg_windows.id'))
    is_processed = Column(Integer, nullable=False, default=0)

    # logger = relationship("Logger", backref="events")
    # event_name = relationship("EventName", backref="events")
    # agg_window = relationship("AggWindow", backref="events")