from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Conversation, Message, User
from ..schemas import Conversation as ConversationSchema, Message as MessageSchema
from ..services import AuthService

router = APIRouter()
auth_service = AuthService()

@router.get("/", response_model=List[ConversationSchema])
async def get_conversations(
    skip: int = 0,
    limit: int = 50,
    channel: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(auth_service.get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get all conversations with optional filtering"""
    query = db.query(Conversation)

    if channel:
        query = query.filter(Conversation.channel == channel)
    if status:
        query = query.filter(Conversation.status == status)

    # Role-based filtering
    if current_user.role not in ["admin", "analyst"]:
        # Non-admin users only see assigned conversations
        query = query.filter(
            (Conversation.assigned_to == current_user.id) |
            (Conversation.assigned_to.is_(None))
        )

    conversations = query.offset(skip).limit(limit).all()
    return conversations

@router.get("/{conversation_id}", response_model=ConversationSchema)
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(auth_service.get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get a specific conversation"""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Check permissions
    if (current_user.role not in ["admin", "analyst"] and
        conversation.assigned_to != current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to view this conversation")

    return conversation

@router.get("/{conversation_id}/messages", response_model=List[MessageSchema])
async def get_conversation_messages(
    conversation_id: int,
    current_user: User = Depends(auth_service.get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get messages for a conversation"""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Check permissions
    if (current_user.role not in ["admin", "analyst"] and
        conversation.assigned_to != current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to view this conversation")

    messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()
    return messages

class AssignConversationRequest(BaseModel):
    user_id: int

@router.post("/{conversation_id}/assign")
async def assign_conversation(
    conversation_id: int,
    request: AssignConversationRequest,
    current_user: User = Depends(auth_service.get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Assign conversation to a user"""
    if not auth_service.check_permissions(current_user, "counselor"):
        raise HTTPException(status_code=403, detail="Not authorized")

    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    conversation.assigned_to = request.user_id
    conversation.status = "assigned"
    db.commit()

    return {"message": "Conversation assigned successfully"}

class ReplyRequest(BaseModel):
    content: str

@router.post("/{conversation_id}/reply")
async def send_reply(
    conversation_id: int,
    request: ReplyRequest,
    current_user: User = Depends(auth_service.get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Send a reply to a conversation"""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Check permissions
    if (current_user.role not in ["admin", "counselor", "sales"] and
        conversation.assigned_to != current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to reply to this conversation")

    # Create message
    message = Message(
        conversation_id=conversation_id,
        direction="outbound",
        content=request.content
    )
    db.add(message)

    # Update conversation status
    conversation.status = "replied"
    db.commit()

    return {"message": "Reply sent successfully"}