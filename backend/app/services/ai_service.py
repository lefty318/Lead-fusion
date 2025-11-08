import openai
from typing import Dict, Any, Optional
from ..config import settings
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        if not settings.openai_api_key:
            logger.warning(
                "OpenAI API key not configured. AI features will be disabled. "
                "Set OPENAI_API_KEY environment variable to enable."
            )
            self.client = None
        else:
            try:
                self.client = openai.OpenAI(api_key=settings.openai_api_key)
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                self.client = None
        self.model = settings.openai_model

    def _check_client(self) -> bool:
        """Check if OpenAI client is available"""
        if self.client is None:
            logger.error("OpenAI client not initialized. Check OPENAI_API_KEY configuration.")
            return False
        return True

    def process_message(self, message_text: str) -> Dict[str, Any]:
        """Process message for intent, sentiment, lead scoring, and reply generation"""
        if not self._check_client():
            return {
                "intent": "general",
                "sentiment": 0.0,
                "confidence": 0.0,
                "lead_score": 0.0,
                "reply": None,
                "urgency": False
            }
        
        try:
            # Intent classification and sentiment analysis
            intent_response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an AI assistant for a student recruitment platform. Classify the intent of the incoming message and analyze sentiment.

Return JSON with:
- intent: one of [enquiry, complaint, enrollment, technical, general, urgent]
- sentiment: float between -1 (very negative) and 1 (very positive)
- confidence: float between 0 and 1
- urgency: boolean indicating if immediate human attention needed"""
                    },
                    {
                        "role": "user",
                        "content": message_text
                    }
                ],
                temperature=0.2,
                max_tokens=200
            )

            intent_data = self._parse_json_response(intent_response.choices[0].message.content)

            # Lead scoring
            lead_score = self._calculate_lead_score(message_text, intent_data)

            # Generate reply if appropriate
            reply = None
            if intent_data.get("intent") in ["enquiry", "general"] and intent_data.get("confidence", 0) > 0.7:
                reply = self._generate_reply(message_text, intent_data)

            return {
                "intent": intent_data.get("intent"),
                "sentiment": intent_data.get("sentiment", 0.0),
                "confidence": intent_data.get("confidence", 0.0),
                "lead_score": lead_score,
                "reply": reply,
                "urgency": intent_data.get("urgency", False)
            }

        except openai.AuthenticationError as e:
            logger.error(f"OpenAI authentication error: {e}. Check your API key.")
            return {
                "intent": "general",
                "sentiment": 0.0,
                "confidence": 0.0,
                "lead_score": 0.0,
                "reply": None,
                "urgency": False
            }
        except openai.RateLimitError as e:
            logger.warning(f"OpenAI rate limit exceeded: {e}")
            return {
                "intent": "general",
                "sentiment": 0.0,
                "confidence": 0.3,
                "lead_score": 0.0,
                "reply": None,
                "urgency": False
            }
        except Exception as e:
            logger.error(f"AI processing error: {e}")
            return {
                "intent": "general",
                "sentiment": 0.0,
                "confidence": 0.5,
                "lead_score": 0.0,
                "reply": None,
                "urgency": False
            }

    def extract_lead_info(self, message_text: str) -> Dict[str, str]:
        """Extract lead information from message"""
        if not self._check_client():
            return {}
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """Extract lead information from the message. Return JSON with:
- name: person's name if mentioned
- phone: phone number if mentioned
- email: email address if mentioned
- program_interest: program/course they're interested in"""
                    },
                    {
                        "role": "user",
                        "content": message_text
                    }
                ],
                temperature=0.1,
                max_tokens=200
            )

            return self._parse_json_response(response.choices[0].message.content)

        except openai.AuthenticationError as e:
            logger.error(f"OpenAI authentication error during lead extraction: {e}")
            return {}
        except Exception as e:
            logger.error(f"Lead extraction error: {e}")
            return {}

    def _calculate_lead_score(self, message_text: str, intent_data: Dict[str, Any]) -> float:
        """Calculate lead score based on message content and intent"""
        score = 0.0

        # Intent-based scoring
        intent_scores = {
            "enrollment": 0.9,
            "enquiry": 0.7,
            "general": 0.3,
            "complaint": 0.2,
            "technical": 0.1,
            "urgent": 0.8
        }
        score += intent_scores.get(intent_data.get("intent", "general"), 0.0)

        # Keyword-based scoring
        high_value_keywords = ["enroll", "admission", "apply", "interested", "join"]
        medium_value_keywords = ["info", "details", "courses", "programs"]

        message_lower = message_text.lower()
        if any(kw in message_lower for kw in high_value_keywords):
            score += 0.3
        elif any(kw in message_lower for kw in medium_value_keywords):
            score += 0.1

        # Sentiment adjustment
        sentiment = intent_data.get("sentiment", 0.0)
        score += sentiment * 0.1  # Small adjustment based on sentiment

        return min(max(score, 0.0), 1.0)  # Clamp between 0 and 1

    def _generate_reply(self, message_text: str, intent_data: Dict[str, Any]) -> str:
        """Generate automated reply"""
        if not self._check_client():
            return "Thank you for your message. A representative will get back to you shortly."
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a helpful student recruitment assistant. Generate a friendly, professional response to student inquiries.

Keep responses concise and helpful. If the inquiry is about specific programs or admissions, ask for more details or provide general information.

Always end with an offer to connect with a human representative if needed."""
                    },
                    {
                        "role": "user",
                        "content": f"Intent: {intent_data.get('intent')}\nMessage: {message_text}"
                    }
                ],
                temperature=0.7,
                max_tokens=300
            )

            return response.choices[0].message.content.strip()

        except openai.AuthenticationError as e:
            logger.error(f"OpenAI authentication error during reply generation: {e}")
            return "Thank you for your message. A representative will get back to you shortly."
        except Exception as e:
            logger.error(f"Reply generation error: {e}")
            return "Thank you for your message. A representative will get back to you shortly."

    def _parse_json_response(self, content: str) -> Dict[str, Any]:
        """Parse JSON response from AI, with fallback"""
        try:
            # Try to extract JSON from the response
            import json
            import re

            # Find JSON-like content
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return json.loads(content)
        except:
            # Fallback parsing for non-JSON responses
            return {
                "intent": "general",
                "sentiment": 0.0,
                "confidence": 0.5,
                "urgency": False
            }