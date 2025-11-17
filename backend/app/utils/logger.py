import logging
import json
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import AnalyticsEvent

class AuditLogger:
    def __init__(self):
        self.logger = logging.getLogger('omnilead_audit')
        self.logger.setLevel(logging.INFO)

        # Create console handler
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)

        # Add handler to logger
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def log_user_action(self, db: Session, user_id: int, action: str, resource: str, resource_id: int = None, details: dict = None):
        """Log user actions for audit trail"""
        log_data = {
            'user_id': user_id,
            'action': action,
            'resource': resource,
            'resource_id': resource_id,
            'details': details or {},
            'timestamp': datetime.utcnow().isoformat()
        }

        # Log to file
        self.logger.info(f"USER_ACTION: {json.dumps(log_data)}")

        # Store in database
        try:
            event = AnalyticsEvent(
                event_type='user_action',
                user_id=user_id,
                data=json.dumps(log_data)
            )
            db.add(event)
            db.commit()
        except Exception as e:
            self.logger.error(f"Failed to store audit log: {e}")

    def log_conversation_event(self, db: Session, conversation_id: int, event_type: str, details: dict = None):
        """Log conversation-related events"""
        log_data = {
            'conversation_id': conversation_id,
            'event_type': event_type,
            'details': details or {},
            'timestamp': datetime.utcnow().isoformat()
        }

        self.logger.info(f"CONVERSATION_EVENT: {json.dumps(log_data)}")

        try:
            event = AnalyticsEvent(
                event_type='conversation_event',
                conversation_id=conversation_id,
                data=json.dumps(log_data)
            )
            db.add(event)
            db.commit()
        except Exception as e:
            self.logger.error(f"Failed to store conversation log: {e}")

    def log_ai_decision(self, db: Session, conversation_id: int, decision: str, confidence: float, details: dict = None):
        """Log AI decision making for compliance"""
        log_data = {
            'conversation_id': conversation_id,
            'decision': decision,
            'confidence': confidence,
            'details': details or {},
            'timestamp': datetime.utcnow().isoformat()
        }

        self.logger.info(f"AI_DECISION: {json.dumps(log_data)}")

        try:
            event = AnalyticsEvent(
                event_type='ai_decision',
                conversation_id=conversation_id,
                data=json.dumps(log_data)
            )
            db.add(event)
            db.commit()
        except Exception as e:
            self.logger.error(f"Failed to store AI decision log: {e}")

    def log_message_processing(self, db: Session, message_id: int, processing_time: float, success: bool, error: str = None):
        """Log message processing metrics"""
        log_data = {
            'message_id': message_id,
            'processing_time': processing_time,
            'success': success,
            'error': error,
            'timestamp': datetime.utcnow().isoformat()
        }

        self.logger.info(f"MESSAGE_PROCESSING: {json.dumps(log_data)}")

# Global audit logger instance
audit_logger = AuditLogger()

def get_logger(name: str):
    """Get a logger instance for the given name"""
    return logging.getLogger(name)