"""
YouTube transcript extraction service using youtube-transcript-api.
"""

import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)


class InvalidURLError(Exception):
    """Raised when the YouTube URL is invalid."""
    pass


class NoTranscriptError(Exception):
    """Raised when no transcript is available for the video."""
    pass


class VideoUnavailableError(Exception):
    """Raised when the video is private or unavailable."""
    pass


def extract_video_id(url: str) -> str:
    """
    Extract the video ID from various YouTube URL formats.
    
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    """
    patterns = [
        r"(?:v=|/)([\w-]{11})(?:\?|&|$|#)",
        r"youtu\.be/([\w-]{11})",
        r"embed/([\w-]{11})",
        r"shorts/([\w-]{11})",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    raise InvalidURLError(f"Could not extract video ID from URL: {url}")


def format_timestamp(seconds: float) -> str:
    """Convert seconds to MM:SS or HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def get_transcript(video_id: str) -> list[dict]:
    """
    Fetch the transcript for a YouTube video.
    
    Returns a list of dicts with 'text', 'start', and 'duration' keys.
    The 'start' is converted to a human-readable timestamp.
    """
    try:
        transcript_list = YouTubeTranscriptApi().list(video_id)
        
        # Try to get English transcript first, fall back to any available
        try:
            transcript = transcript_list.find_transcript(["en"])
        except NoTranscriptFound:
            # Fall back to auto-generated or first available
            transcript = transcript_list.find_generated_transcript(["en"])
        
        entries = transcript.fetch()
        
        result = []
        for entry in entries:
            result.append({
                "text": entry.text,
                "start": entry.start,
                "duration": entry.duration,
                "timestamp": format_timestamp(entry.start),
            })
        
        return result
        
    except TranscriptsDisabled:
        raise NoTranscriptError("Transcripts are disabled for this video")
    except NoTranscriptFound:
        raise NoTranscriptError("No transcript available for this video")
    except VideoUnavailable:
        raise VideoUnavailableError("Video is private or unavailable")
    except Exception as e:
        raise NoTranscriptError(f"Failed to fetch transcript: {str(e)}")


def get_video_duration(transcript: list[dict]) -> str:
    """Estimate video duration from the last transcript entry."""
    if not transcript:
        return "00:00"
    
    last_entry = transcript[-1]
    total_seconds = last_entry["start"] + last_entry["duration"]
    return format_timestamp(total_seconds)
