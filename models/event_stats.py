from sqlalchemy import Column, Integer, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for declarative models
Base = declarative_base()

class EventStats(Base):
    __tablename__ = 'event_stats'
    event_id = Column(Integer, primary_key=True)
    insertion_ts = Column(TIMESTAMP(timezone=True), server_default=func.now())
    ev_ts = Column(TIMESTAMP(timezone=True))

    # lg_id = Column(Integer, ForeignKey('loggers.logger_id'))
    # en_id = Column(Integer, ForeignKey('EVENT_NAMES.event_name_id'))

    aw_id = Column(Integer, ForeignKey("agg_windows.agg_window_id"))
    parent = relationship("AggWindows", back_populates="children")