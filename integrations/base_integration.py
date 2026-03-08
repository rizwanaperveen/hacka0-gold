"""
Base Integration - Abstract base class for all external integrations

Provides common functionality and interface for:
- API authentication
- Request/response handling
- Rate limiting
- Error handling
- Audit logging
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class BaseIntegration(ABC):
    """
    Abstract base class for all external API integrations.

    Integrations provide clean interfaces to external services,
    handling authentication, rate limiting, and error recovery.
    """

    def __init__(
        self,
        name: str,
        config: Dict[str, Any] = None,
        audit_logger=None
    ):
        self.name = name
        self.config = config or {}
        self.audit_logger = audit_logger

        self.logger = logging.getLogger(f"{self.__class__.__name__}")

        # Integration state
        self.state = {
            "connected": False,
            "authenticated": False,
            "initialized": False,
            "last_request": None,
            "total_requests": 0,
            "failed_requests": 0
        }

        # Rate limiting
        self.rate_limit = {
            "requests_per_minute": 60,
            "requests_per_hour": 1000,
            "current_minute_count": 0,
            "current_hour_count": 0
        }

        self.logger.info(f"Integration '{name}' initialized")

    @abstractmethod
    async def initialize(self) -> bool:
        """
        Initialize the integration (authenticate, setup connections).

        Returns:
            True if initialization successful
        """
        pass

    @abstractmethod
    async def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection to the external service.

        Returns:
            Connection test result
        """
        pass

    async def _check_rate_limit(self) -> bool:
        """Check if request is within rate limits."""
        # Simple rate limit check - can be enhanced with token bucket algorithm
        if self.rate_limit["current_minute_count"] >= self.rate_limit["requests_per_minute"]:
            self.logger.warning("Rate limit exceeded for current minute")
            return False

        return True

    async def _track_request(self, success: bool = True):
        """Track request statistics."""
        self.state["total_requests"] += 1
        self.state["last_request"] = datetime.now().isoformat()

        if not success:
            self.state["failed_requests"] += 1

        self.rate_limit["current_minute_count"] += 1
        self.rate_limit["current_hour_count"] += 1

    def get_status(self) -> Dict[str, Any]:
        """Get integration status."""
        return {
            "name": self.name,
            "connected": self.state["connected"],
            "authenticated": self.state["authenticated"],
            "total_requests": self.state["total_requests"],
            "failed_requests": self.state["failed_requests"],
            "success_rate": self._calculate_success_rate()
        }

    def _calculate_success_rate(self) -> float:
        """Calculate request success rate."""
        if self.state["total_requests"] == 0:
            return 100.0

        successful = self.state["total_requests"] - self.state["failed_requests"]
        return (successful / self.state["total_requests"]) * 100

    async def shutdown(self):
        """Shutdown the integration gracefully."""
        self.logger.info(f"Shutting down {self.name} integration")
        self.state["connected"] = False
        self.state["authenticated"] = False
