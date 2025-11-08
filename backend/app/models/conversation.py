from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)  # WhatsApp/Facebook message ID
    channel = Column(String)  # whatsapp, facebook, instagram
    sender_id = Column(String, index=True)
    sender_name = Column(String)
    recipient_id = Column(String)
    message_text = Column(Text)
    message_type = Column(String)  # text, image, video, etc.
    timestamp = Column(DateTime(timezone=True))
    lead_score = Column(Float, default=0.0)
    sentiment = Column(Float, default=0.0)  # -1 to 1
    intent = Column(String)
    ai_confidence = Column(Float, default=0.0)
    needs_human = Column(Boolean, default=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, default="open")  # open, closed, escalated
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    assigned_user = relationship("User")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    direction = Column(String)  # inbound, outbound
    content = Column(Text)
    content_type = Column(String, default="text")
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    read_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")