import firebase_admin
from firebase_admin import messaging, credentials
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
from typing import List
from sqlalchemy.orm import Session
from ..models import User, Conversation
from ..config import settings

class NotificationService:
    def __init__(self):
        # Initialize Firebase for push notifications
        if settings.firebase_server_key:
            try:
                cred = credentials.Certificate(settings.firebase_server_key)
                firebase_admin.initialize_app(cred)
            except:
                pass

        # Initialize Twilio for SMS
        if settings.twilio_account_sid and settings.twilio_auth_token:
            self.twilio_client = Client(
                settings.twilio_account_sid,
                settings.twilio_auth_token
            )
        else:
            self.twilio_client = None

    def send_escalation_notification(self, conversation: Conversation, db: Session):
        """Send notifications when conversation needs human attention"""
        # Get users who should be notified (based on role and availability)
        users_to_notify = db.query(User).filter(
            User.role.in_(["admin", "sales", "counselor"]),
            User.is_active == True
        ).all()

        message = f"New escalated conversation from {conversation.sender_name} ({conversation.channel})"

        for user in users_to_notify:
            self._send_push_notification(user, message, conversation.id)
            self._send_email_notification(user, "Escalated Conversation", message, conversation)
            self._send_sms_notification(user, message)

    def send_new_lead_notification(self, lead, db: Session):
        """Send notifications for new high-value leads"""
        if lead.score >= 0.7:
            users_to_notify = db.query(User).filter(
                User.role.in_(["admin", "sales"]),
                User.is_active == True
            ).all()

            message = f"High-value lead: {lead.name} - Score: {lead.score:.2f}"

            for user in users_to_notify:
                self._send_push_notification(user, message, lead.id)
                self._send_email_notification(user, "New High-Value Lead", message, lead)

    def send_missed_message_notification(self, conversation: Conversation, db: Session):
        """Send notifications for missed messages"""
        users_to_notify = db.query(User).filter(
            User.role.in_(["admin", "sales", "counselor"]),
            User.is_active == True
        ).all()

        message = f"Missed message from {conversation.sender_name} ({conversation.channel})"

        for user in users_to_notify:
            self._send_push_notification(user, message, conversation.id)

    def _send_push_notification(self, user: User, message: str, reference_id: int):
        """Send push notification via Firebase"""
        try:
            if not hasattr(firebase_admin, '_apps') or not firebase_admin._apps:
                return

            # This would require storing FCM tokens for users
            # For now, we'll skip the actual implementation
            print(f"Push notification to {user.email}: {message}")
        except Exception as e:
            print(f"Push notification error: {e}")

    def _send_email_notification(self, user: User, subject: str, message: str, reference=None):
        """Send email notification via SendGrid"""
        try:
            if not settings.sendgrid_api_key:
                return

            # SendGrid implementation would go here
            # For now, using SMTP as fallback
            msg = MIMEMultipart()
            msg['From'] = "noreply@omnilead.com"
            msg['To'] = user.email
            msg['Subject'] = subject

            body = f"""
            {message}

            Please log in to OmniLead to view details.
            """

            if reference:
                body += f"\n\nReference ID: {reference.id}"

            msg.attach(MIMEText(body, 'plain'))

            # This would need SMTP server configuration
            print(f"Email notification to {user.email}: {subject}")
        except Exception as e:
            print(f"Email notification error: {e}")

    def _send_sms_notification(self, user: User, message: str):
        """Send SMS notification via Twilio"""
        try:
            if not self.twilio_client or not settings.twilio_phone_number:
                return

            # This would require storing phone numbers for users
            # For now, we'll skip
            print(f"SMS notification: {message}")
        except Exception as e:
            print(f"SMS notification error: {e}")

    def send_bulk_notification(self, users: List[User], title: str, message: str):
        """Send bulk notifications to multiple users"""
        for user in users:
            self._send_push_notification(user, message, 0)
            self._send_email_notification(user, title, message)