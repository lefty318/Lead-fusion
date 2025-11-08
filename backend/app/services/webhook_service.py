import hmac
import hashlib
import json
from typing import Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Conversation, Message, Lead
from ..database import get_db
from .ai_service import AIService
from .notification_service import NotificationService

class WebhookService:
    def __init__(self):
        self.ai_service = AIService()
        self.notification_service = NotificationService()

    def verify_whatsapp_signature(self, payload: bytes, signature: str, secret: str) -> bool:
        expected_signature = hmac.new(
            secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(f"sha256={expected_signature}", signature)

    def process_whatsapp_message(self, data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """Process incoming WhatsApp message"""
        try:
            entry = data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            messages = changes.get("value", {}).get("messages", [])

            for message in messages:
                if message.get("type") == "text":
                    conversation = self._create_or_update_conversation(
                        message, "whatsapp", db
                    )
                    self._process_message_with_ai(conversation, db)
                    return {"status": "processed", "conversation_id": conversation.id}

            return {"status": "no_text_message"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def process_facebook_message(self, data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """Process incoming Facebook Messenger message"""
        try:
            messaging = data.get("entry", [{}])[0].get("messaging", [])

            for event in messaging:
                if event.get("message"):
                    message = event["message"]
                    if message.get("text"):
                        conversation = self._create_or_update_conversation(
                            {
                                "id": event["sender"]["id"],
                                "from": event["sender"]["id"],
                                "text": {"body": message["text"]},
                                "timestamp": event["timestamp"]
                            },
                            "facebook",
                            db
                        )
                        self._process_message_with_ai(conversation, db)
                        return {"status": "processed", "conversation_id": conversation.id}

            return {"status": "no_text_message"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def process_instagram_message(self, data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """Process incoming Instagram DM"""
        # Similar to Facebook but with Instagram-specific fields
        return self.process_facebook_message(data, db)

    def _create_or_update_conversation(self, message: Dict[str, Any], channel: str, db: Session) -> Conversation:
        """Create or update conversation from message data"""
        external_id = message.get("id")
        sender_id = message.get("from")
        sender_name = message.get("profile", {}).get("name", "Unknown")

        # Extract message text based on channel
        if channel == "whatsapp":
            message_text = message.get("text", {}).get("body", "")
        else:
            message_text = message.get("text", {}).get("body", "")

        timestamp = datetime.fromtimestamp(int(message.get("timestamp", 0)) / 1000)

        # Find existing conversation or create new one
        conversation = db.query(Conversation).filter(
            Conversation.sender_id == sender_id,
            Conversation.channel == channel
        ).first()

        if not conversation:
            conversation = Conversation(
                external_id=external_id,
                channel=channel,
                sender_id=sender_id,
                sender_name=sender_name,
                recipient_id="business",  # Our business account
                message_text=message_text,
                timestamp=timestamp
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        else:
            conversation.message_text = message_text
            conversation.timestamp = timestamp
            db.commit()

        # Add message to conversation
        db_message = Message(
            conversation_id=conversation.id,
            direction="inbound",
            content=message_text
        )
        db.add(db_message)
        db.commit()

        return conversation

    def _process_message_with_ai(self, conversation: Conversation, db: Session):
        """Process message with AI for classification and response"""
        try:
            # AI processing
            ai_result = self.ai_service.process_message(conversation.message_text)

            # Update conversation with AI results
            conversation.intent = ai_result.get("intent")
            conversation.sentiment = ai_result.get("sentiment", 0.0)
            conversation.lead_score = ai_result.get("lead_score", 0.0)
            conversation.ai_confidence = ai_result.get("confidence", 0.0)

            # Check escalation rules
            if self._should_escalate(conversation):
                conversation.needs_human = True
                conversation.status = "escalated"
                self.notification_service.send_escalation_notification(conversation, db)

            # Auto-reply if confidence is high enough
            elif conversation.ai_confidence >= 0.7:
                reply = ai_result.get("reply")
                if reply:
                    self._send_auto_reply(conversation, reply, db)

            db.commit()

            # Extract lead information if applicable
            if conversation.intent in ["enquiry", "enrollment"]:
                self._extract_lead_info(conversation, db)

        except Exception as e:
            print(f"AI processing error: {e}")

    def _should_escalate(self, conversation: Conversation) -> bool:
        """Check if conversation should be escalated to human"""
        if conversation.ai_confidence < 0.65:
            return True
        if conversation.sentiment < -0.5:
            return True
        if any(keyword in conversation.message_text.lower() for keyword in
               ["refund", "legal", "complaint", "technical", "urgent"]):
            return True
        return False

    def _send_auto_reply(self, conversation: Conversation, reply: str, db: Session):
        """Send automated reply"""
        # This would integrate with the actual messaging APIs
        # For now, just log the reply
        db_message = Message(
            conversation_id=conversation.id,
            direction="outbound",
            content=reply
        )
        db.add(db_message)
        db.commit()

    def _extract_lead_info(self, conversation: Conversation, db: Session):
        """Extract and save lead information"""
        lead_info = self.ai_service.extract_lead_info(conversation.message_text)

        if lead_info.get("name") or lead_info.get("phone"):
            lead = Lead(
                conversation_id=conversation.id,
                name=lead_info.get("name"),
                phone=lead_info.get("phone"),
                email=lead_info.get("email"),
                program_interest=lead_info.get("program_interest"),
                score=conversation.lead_score
            )
            db.add(lead)
            db.commit()