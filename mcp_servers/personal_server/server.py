"""
Personal MCP Server - FastAPI server for personal domain operations

Provides RESTful API endpoints for:
- Email operations
- Calendar management
- Task management
- Personal reminders
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from mcp_servers.base_server import BaseMCPServer
from mcp_servers.personal_server.routes import email_router, calendar_router, task_router

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PersonalMCPServer")


class PersonalMCPServer(BaseMCPServer):
    """Personal domain MCP server."""

    def __init__(self):
        super().__init__(
            name="personal",
            version="1.0.0",
            port=8001,
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
        self.app.include_router(email_router)
        self.app.include_router(calendar_router)
        self.app.include_router(task_router)

        logger.info("Personal server routes registered")


# Create app instance
app = PersonalMCPServer().get_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "mcp_servers.personal_server.server:app",
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
