"""
Business MCP Server - FastAPI server for business domain operations

Provides RESTful API endpoints for:
- CRM operations
- Analytics and reporting
- Invoicing
- Business intelligence
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from mcp_servers.base_server import BaseMCPServer
from mcp_servers.business_server.routes import crm_router, analytics_router

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BusinessMCPServer")


class BusinessMCPServer(BaseMCPServer):
    """Business domain MCP server."""

    def __init__(self):
        super().__init__(
            name="business",
            version="1.0.0",
            port=8002,
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
        self.app.include_router(crm_router)
        self.app.include_router(analytics_router)

        logger.info("Business server routes registered")


# Create app instance
app = BusinessMCPServer().get_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "mcp_servers.business_server.server:app",
        host="0.0.0.0",
        port=8002,
        log_level="info"
    )
