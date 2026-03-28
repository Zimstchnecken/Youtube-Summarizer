"""
Pydantic models for request/response schemas.
"""

from pydantic import BaseModel, field_validator
from typing import List
import re


class SummarizeRequest(BaseModel):
    """Request body for the summarize endpoint."""
    url: str

    @field_validator("url")
    @classmethod
    def validate_youtube_url(cls, v: str) -> str:
        """Validate that the URL is a valid YouTube URL."""
        youtube_patterns = [
            r"^https?://(www\.)?youtube\.com/watch\?v=[\w-]{11}",
            r"^https?://youtu\.be/[\w-]{11}",
            r"^https?://(www\.)?youtube\.com/embed/[\w-]{11}",
            r"^https?://(www\.)?youtube\.com/shorts/[\w-]{11}",
        ]
        if not any(re.match(pattern, v) for pattern in youtube_patterns):
            raise ValueError("Invalid YouTube URL format")
        return v


class SummaryPoint(BaseModel):
    """A single summary point with timestamp."""
    timestamp: str
    point: str


class SummarizeResponse(BaseModel):
    """Response body for the summarize endpoint."""
    title: str
    duration: str
    summary: List[SummaryPoint]
    video_id: str
    url: str


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str
