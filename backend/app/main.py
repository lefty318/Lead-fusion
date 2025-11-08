from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import socketio
import uvicorn
from .database import get_db, engine
from .models import Base
from .services import WebhookService, AuthService
from .routes import auth, conversations, analytics, webhooks
from .config import settings

# Note: In production, use Alembic migrations instead of create_all
# Run: alembic upgrade head
# For development only:
if settings.environment == "development":
    Base.metadata.create_all(bind=engine)

# Initialize services
webhook_service = WebhookService()
auth_service = AuthService()

# Create FastAPI app
app = FastAPI(title="OmniLead API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.IO setup
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, app)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["conversations"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])

# Note: get_current_user dependency is now in AuthService.get_current_user_dependency

# Socket.IO events
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def join_conversation(sid, data):
    """Join a conversation room for real-time updates"""
    conversation_id = data.get('conversation_id')
    if conversation_id:
        await sio.enter_room(sid, f"conversation_{conversation_id}")
        print(f"Client {sid} joined conversation {conversation_id}")

@sio.event
async def leave_conversation(sid, data):
    """Leave a conversation room"""
    conversation_id = data.get('conversation_id')
    if conversation_id:
        await sio.leave_room(sid, f"conversation_{conversation_id}")
        print(f"Client {sid} left conversation {conversation_id}")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app.main:socket_app", host="0.0.0.0", port=8000, reload=True)