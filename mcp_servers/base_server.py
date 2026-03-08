"""
Base MCP Server - Abstract base class for MCP servers

Provides common functionality and interface for:
- FastAPI app setup
- Route registration
- Middleware configuration
- Health checks
- Lifecycle management
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from fastapi import FastAPI


class BaseMCPServer(ABC):
    """
    Abstract base class for MCP (Model Context Protocol) servers.

    MCP servers provide RESTful APIs for domain-specific operations,
    enabling modular deployment and scaling.
    """

    def __init__(
        self,
        name: str,
        version: str = "1.0.0",
        port: int = 8000,
        host: str = "0.0.0.0"
    ):
        self.name = name
        self.version = version
        self.port = port
        self.host = host

        self.logger = logging.getLogger(f"{self.__class__.__name__}")

        # Create FastAPI app
        self.app = FastAPI(
            title=f"{name} MCP Server",
            description=f"MCP server for {name} domain operations",
            version=version
        )

        # Server state
        self.state = {
            "running": False,
            "started_at": None,
            "total_requests": 0
        }

        # Register default routes
        self._register_default_routes()

        self.logger.info(f"MCP Server '{name}' initialized on {host}:{port}")

    def _register_default_routes(self):
        """Register default routes (health check, status)."""

        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {
                "status": "healthy",
                "service": self.name,
                "version": self.version
            }

        @self.app.get("/status")
        async def status():
            """Server status endpoint."""
            return {
                "name": self.name,
                "version": self.version,
                "running": self.state["running"],
                "started_at": self.state["started_at"]
            }

    @abstractmethod
    def register_routes(self):
        """Register domain-specific routes."""
        pass

    def get_app(self) -> FastAPI:
        """Get the FastAPI application instance."""
        return self.app

    async def start(self):
        """Start the server."""
        self.logger.info(f"Starting {self.name} MCP Server...")
        self.state["running"] = True
        self.state["started_at"] = __import__('datetime').datetime.now().isoformat()

    async def stop(self):
        """Stop the server."""
        self.logger.info(f"Stopping {self.name} MCP Server...")
        self.state["running"] = False

    def get_status(self) -> Dict[str, Any]:
        """Get server status."""
        return {
            "name": self.name,
            "version": self.version,
            "port": self.port,
            "running": self.state["running"],
            "started_at": self.state["started_at"]
        }
