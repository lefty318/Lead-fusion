from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services import WebhookService

router = APIRouter()
webhook_service = WebhookService()

@router.post("/whatsapp")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle WhatsApp webhook"""
    try:
        data = await request.json()
        signature = request.headers.get("X-Hub-Signature-256")

        # Verify signature if secret is configured
        if hasattr(request.app.state, 'whatsapp_secret') and request.app.state.whatsapp_secret:
            if not webhook_service.verify_whatsapp_signature(
                await request.body(), signature, request.app.state.whatsapp_secret
            ):
                raise HTTPException(status_code=401, detail="Invalid signature")

        result = webhook_service.process_whatsapp_message(data, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/facebook")
async def facebook_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Facebook Messenger webhook"""
    try:
        data = await request.json()
        result = webhook_service.process_facebook_message(data, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/instagram")
async def instagram_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Instagram webhook"""
    try:
        data = await request.json()
        result = webhook_service.process_instagram_message(data, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/whatsapp")
async def whatsapp_verify(request: Request):
    """WhatsApp webhook verification"""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    # Verify token (should match configured token)
    if mode == "subscribe" and token == "your_verify_token":
        return int(challenge)
    else:
        raise HTTPException(status_code=403, detail="Verification failed")