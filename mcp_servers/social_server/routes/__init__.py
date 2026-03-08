"""
Social Server Routes - API route handlers
"""

from .facebook_routes import router as facebook_router
from .instagram_routes import router as instagram_router
from .twitter_routes import router as twitter_router
from .linkedin_routes import router as linkedin_router

__all__ = [
    "facebook_router",
    "instagram_router",
    "twitter_router",
    "linkedin_router",
]
