# Export modules so they can be imported as: from .routes import auth, conversations, analytics, webhooks
from . import auth
from . import conversations
from . import analytics
from . import webhooks

# Also export routers for direct access if needed
from .auth import router as auth_router
from .conversations import router as conversations_router
from .analytics import router as analytics_router
from .webhooks import router as webhooks_router