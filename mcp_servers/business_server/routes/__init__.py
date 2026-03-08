"""
Business Server Routes - API route handlers
"""

from .crm_routes import router as crm_router
from .analytics_routes import router as analytics_router

__all__ = ["crm_router", "analytics_router"]
