"""
Social MCP Server - FastAPI server for social media operations

Provides RESTful API endpoints for:
- Facebook operations
- Instagram operations
- Twitter operations
- LinkedIn operations
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from mcp_servers.base_server import BaseMCPServer
from mcp_servers.social_server.routes import (
    facebook_router,
    instagram_router,
    twitter_router,
    linkedin_router
)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SocialMCPServer")


class SocialMCPServer(BaseMCPServer):
    """Social media MCP server."""

    def __init__(self):
        super().__init__(
            name="social",
            version="1.0.0",
            port=8003,
            host="0.0.0.0"
        )

        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Register routes
        self.register_routes()

    def register_routes(self):
        """Register domain-specific routes."""
        self.app.include_router(facebook_router)
        self.app.include_router(instagram_router)
        self.app.include_router(twitter_router)
        self.app.include_router(linkedin_router)

        logger.info("Social server routes registered")


# Create app instance
app = SocialMCPServer().get_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "mcp_servers.social_server.server:app",
        host="0.0.0.0",
        port=8003,
        log_level="info"
    )
