from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    full_name: str
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ConversationBase(BaseModel):
    channel: str
    sender_id: str
    sender_name: str
    message_text: str

class Conversation(ConversationBase):
    id: int
    lead_score: float
    sentiment: float
    intent: Optional[str]
    ai_confidence: float
    needs_human: bool
    status: str
    timestamp: datetime

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    content: str
    content_type: str = "text"

class Message(MessageBase):
    id: int
    conversation_id: int
    direction: str
    sent_at: datetime

    class Config:
        from_attributes = True

class LeadBase(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    program_interest: Optional[str]
    score: float

class Lead(LeadBase):
    id: int
    conversation_id: int
    status: str
    assigned_to: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True