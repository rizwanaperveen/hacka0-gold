"""
Personal Server Routes - API route handlers
"""

from .email_routes import router as email_router
from .calendar_routes import router as calendar_router
from .task_routes import router as task_router

__all__ = ["email_router", "calendar_router", "task_router"]
