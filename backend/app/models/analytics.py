from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.sql import func
from ..database import Base

class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String)  # message_received, lead_created, conversation_closed, etc.
    user_id = Column(Integer, nullable=True)
    conversation_id = Column(Integer, nullable=True)
    lead_id = Column(Integer, nullable=True)
    channel = Column(String)
    data = Column(Text)  # JSON data
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)  # daily, weekly, monthly
    data = Column(Text)  # JSON report data
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer)