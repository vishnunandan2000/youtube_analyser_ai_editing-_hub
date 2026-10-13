"""
OAuth 2.0 and YouTube Analytics API Authentication Handler.
Manages owner-authorized YouTube Analytics credentials and states.
"""

from typing import Dict, Any, Optional
from config import settings
from utils.logging_config import logger

class OAuthService:
    def __init__(self):
        self.client_secrets_file = settings.youtube_client_secrets_file
        self.is_authenticated = False
        self.authenticated_channel_id: Optional[str] = None

    def get_auth_status(self) -> Dict[str, Any]:
        """Return diagnostic status of YouTube Analytics OAuth."""
        if not self.client_secrets_file:
            return {
                "configured": False,
                "authenticated": False,
                "channel_id": None,
                "message": "OAuth client secrets file not configured (YOUTUBE_CLIENT_SECRETS_FILE empty)."
            }
        return {
            "configured": True,
            "authenticated": self.is_authenticated,
            "channel_id": self.authenticated_channel_id,
            "message": "OAuth client secrets configured. Channel authenticated." if self.is_authenticated else "OAuth configured, awaiting user authorization token."
        }

    def simulate_mock_auth_for_demo(self, channel_id: str = "UC_DEMO_CREATOR") -> bool:
        """Allows enabling authenticated mode in testing or local demonstration."""
        self.is_authenticated = True
        self.authenticated_channel_id = channel_id
        logger.info(f"Demo authorization granted for channel: {channel_id}")
        return True

oauth_service = OAuthService()
