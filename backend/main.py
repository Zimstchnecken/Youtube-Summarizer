"""
YouTube Video Summarizer — FastAPI Backend

Main entry point with routes, CORS, rate limiting, and error handling.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from config import FRONTEND_ORIGINS, RATE_LIMIT
from models import SummarizeRequest, SummarizeResponse, SummaryPoint, ErrorResponse
from services.youtube import (
    extract_video_id,
    get_transcript,
    get_video_duration,
    InvalidURLError,
    NoTranscriptError,
    VideoUnavailableError,
)
from services.summarizer import (
    summarize_transcript,
    SummarizationError,
    RateLimitError,
)
from services.cache import cache
from utils.chunker import chunk_transcript

# ── Logging ────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ── Rate Limiter ───────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)

# ── App ────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 YouTube Summarizer API starting up")
    yield
    logger.info("👋 YouTube Summarizer API shutting down")

app = FastAPI(
    title="YouTube Video Summarizer API",
    description="AI-powered YouTube video summarization using Google Gemini",
    version="1.0.0",
    lifespan=lifespan,
)

# ── Middleware ─────────────────────────────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routes ─────────────────────────────────────────────────────────
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/api/summarize", response_model=SummarizeResponse)
@limiter.limit(RATE_LIMIT)
async def summarize_video(request: Request, body: SummarizeRequest):
    """
    Summarize a YouTube video given its URL.
    
    Pipeline: validate URL → extract transcript → chunk → summarize → cache
    """
    url = body.url
    
    try:
        # Step 1: Extract video ID
        video_id = extract_video_id(url)
        logger.info(f"Processing video: {video_id}")
        
        # Step 2: Check cache
        cached = cache.get(video_id)
        if cached:
            logger.info(f"Cache hit for video: {video_id}")
            return cached
        
        # Step 3: Get transcript
        transcript = get_transcript(video_id)
        logger.info(f"Transcript fetched: {len(transcript)} entries")
        
        # Step 4: Get video duration
        duration = get_video_duration(transcript)
        
        # Step 5: Chunk transcript
        chunks = chunk_transcript(transcript)
        logger.info(f"Transcript chunked into {len(chunks)} segments")
        
        # Step 6: Summarize via Gemini
        summary_points = summarize_transcript(chunks)
        logger.info(f"Generated {len(summary_points)} summary points")
        
        # Step 7: Build response
        response = SummarizeResponse(
            title=f"YouTube Video ({video_id})",
            duration=duration,
            summary=[
                SummaryPoint(
                    timestamp=p.get("timestamp", "00:00"),
                    point=p.get("point", ""),
                )
                for p in summary_points
                if p.get("point")
            ],
            video_id=video_id,
            url=url,
        )
        
        # Step 8: Cache result
        cache.set(video_id, response)
        logger.info(f"Result cached for video: {video_id}")
        
        return response
        
    except InvalidURLError as e:
        logger.warning(f"Invalid URL: {url} — {e}")
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="Invalid YouTube URL format").model_dump(),
        )
    except NoTranscriptError as e:
        logger.warning(f"No transcript: {video_id} — {e}")
        return JSONResponse(
            status_code=422,
            content=ErrorResponse(detail=str(e)).model_dump(),
        )
    except VideoUnavailableError as e:
        logger.warning(f"Video unavailable: {video_id} — {e}")
        return JSONResponse(
            status_code=403,
            content=ErrorResponse(detail="Video is private or restricted").model_dump(),
        )
    except RateLimitError as e:
        logger.error(f"OpenRouter rate limit hit: {e}")
        return JSONResponse(
            status_code=429,
            content=ErrorResponse(
                detail="Service temporarily unavailable, try again later"
            ).model_dump(),
        )
    except SummarizationError as e:
        logger.error(f"Summarization error: {e}")
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(detail="Failed to summarize video").model_dump(),
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(detail="An unexpected error occurred").model_dump(),
        )
