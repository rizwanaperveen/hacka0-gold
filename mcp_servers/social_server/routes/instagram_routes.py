"""
Instagram Routes - Instagram operation API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/instagram", tags=["instagram"])


class PostRequest(BaseModel):
    image_url: str
    caption: Optional[str] = None


@router.post("/post")
async def create_post(request: PostRequest):
    """Create an Instagram post."""
    return {
        "status": "success",
        "post_id": "ig_post_placeholder",
        "caption": request.caption
    }


@router.get("/media")
async def get_media(limit: int = 10):
    """Get recent media."""
    return {
        "media": [],
        "count": 0
    }


@router.get("/insights")
async def get_insights(metric_names: str):
    """Get account insights."""
    metrics = metric_names.split(",")
    return {
        "metrics": {}
    }
