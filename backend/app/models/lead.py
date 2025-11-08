from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    program_interest = Column(String)
    score = Column(Float, default=0.0)
    status = Column(String, default="new")  # new, contacted, qualified, converted, lost
    priority = Column(String, default="medium")  # low, medium, high
    notes = Column(Text)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    conversation = relationship("Conversation")
    assigned_user = relationship("User")