"""
Summarization service using OpenRouter API.
"""

import json
import logging
import re
from openai import OpenAI

from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    OPENROUTER_FALLBACK_MODELS,
    SYSTEM_PROMPT,
)

logger = logging.getLogger(__name__)

# Configure the OpenRouter API via OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

MODEL_CANDIDATES = []
for model in [OPENROUTER_MODEL, *OPENROUTER_FALLBACK_MODELS]:
    if model not in MODEL_CANDIDATES:
        MODEL_CANDIDATES.append(model)


class SummarizationError(Exception):
    """Raised when summarization fails."""
    pass


class RateLimitError(Exception):
    """Raised when API rate limit is hit."""
    pass


def _to_seconds(timestamp: str) -> int:
    """Convert MM:SS or HH:MM:SS string to seconds for ordering."""
    if not isinstance(timestamp, str):
        return 0

    parts = timestamp.strip().split(":")
    if not parts:
        return 0

    try:
        nums = [int(p) for p in parts]
    except ValueError:
        return 0

    if len(nums) == 3:
        return nums[0] * 3600 + nums[1] * 60 + nums[2]
    if len(nums) == 2:
        return nums[0] * 60 + nums[1]
    if len(nums) == 1:
        return nums[0]
    return 0


def _normalize_timestamp(value: str) -> str:
    """Normalize timestamp to MM:SS or HH:MM:SS."""
    if not isinstance(value, str):
        return "00:00"

    cleaned = value.strip()
    match = re.search(r"(\d{1,2}:\d{2}(?::\d{2})?)", cleaned)
    if match:
        cleaned = match.group(1)

    seconds = _to_seconds(cleaned)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def _cleanup_points(points: list[dict]) -> list[dict]:
    """Normalize, filter, sort, and deduplicate summary points."""
    cleaned = []
    seen = set()

    for point in points:
        ts = _normalize_timestamp(point.get("timestamp", "00:00"))
        text = str(point.get("point", "")).strip()
        if not text:
            continue

        # Collapse whitespace so duplicate detection is stable.
        text = " ".join(text.split())
        key = (ts, text.lower())
        if key in seen:
            continue
        seen.add(key)
        cleaned.append({"timestamp": ts, "point": text})

    cleaned.sort(key=lambda p: _to_seconds(p["timestamp"]))
    return cleaned


def _run_model(messages: list[dict]) -> list[dict]:
    """Run completion across candidate models and return parsed points."""
    saw_rate_limit = False
    last_error = None

    for model in MODEL_CANDIDATES:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2,
            )

            content = response.choices[0].message.content
            if not content:
                logger.warning(f"Empty response from AI for model: {model}")
                continue

            points = _parse_ai_response(content)
            points = _cleanup_points(points)
            if points:
                return points

            logger.warning(f"Parsed empty summary points for model: {model}")

        except Exception as e:
            error_msg = str(e).lower()
            last_error = e

            # Retry with fallback models for common transient/provider issues.
            if (
                "429" in error_msg
                or "rate" in error_msg
                or "quota" in error_msg
                or "404" in error_msg
                or "no endpoints found" in error_msg
            ):
                if "429" in error_msg or "rate" in error_msg or "quota" in error_msg:
                    saw_rate_limit = True
                logger.warning(f"Model {model} failed, trying next fallback: {e}")
                continue

            logger.error(f"API error for model {model}: {e}")
            raise SummarizationError(f"Summarization failed: {str(e)}")

    if saw_rate_limit:
        raise RateLimitError("API rate limit exceeded. Try again later.")

    if last_error:
        raise SummarizationError(f"Summarization failed: {str(last_error)}")

    raise SummarizationError("Summarization failed: all candidate models returned empty output")


def _parse_ai_response(response_text: str) -> list[dict]:
    """
    Parse the AI response text into a list of summary points.
    Handles cases where the response may include markdown code fences.
    """
    text = response_text.strip()
    
    # Remove markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last lines (code fences)
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
        
    # sometimes it starts with ```json
    if text.lower().startswith("json"):
        text = text[4:].strip()
    
    try:
        data = json.loads(text)
        
        # Handle both {"points": [...]} and direct [...]
        if isinstance(data, dict) and "points" in data:
            return data["points"]
        elif isinstance(data, list):
            return data
        else:
            logger.warning(f"Unexpected response structure: {type(data)}")
            return []
            
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse AI response as JSON: {e}")
        logger.error(f"Raw response: {text[:500]}")
        raise SummarizationError("Failed to parse AI response")


def summarize_chunk(chunk_text: str) -> list[dict]:
    """
    Summarize a single transcript chunk using OpenRouter.
    
    Args:
        chunk_text: The transcript text with timestamps to summarize.
        
    Returns:
        List of dicts with 'timestamp' and 'point' keys.
    """
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        "You are creating a high-quality timeline summary for a YouTube video transcript chunk.\n"
        "Return ONLY a JSON array of objects with this exact shape: "
        "[{\"timestamp\":\"MM:SS or HH:MM:SS\",\"point\":\"...\"}].\n\n"
        "Quality requirements:\n"
        "- Produce 8 to 14 points for this chunk when content allows.\n"
        "- Keep chronological order.\n"
        "- Use concrete details: what happened, why it matters, and important examples, names, or numbers.\n"
        "- Each point should be 1 to 2 sentences and easy to scan.\n"
        "- Skip filler (greetings, sponsor plugs, repeated subscribe reminders).\n"
        "- Use timestamps that exist in the transcript (nearest valid one).\n"
        "- No markdown, no commentary, no extra keys.\n\n"
        f"Transcript chunk:\n{chunk_text}"
    )

    return _run_model([{"role": "user", "content": prompt}])


def refine_summary(points: list[dict]) -> list[dict]:
    """Consolidate chunk summaries into a coherent final timeline."""
    if not points:
        return []

    points = _cleanup_points(points)
    if len(points) <= 3:
        return points

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        "You are given draft timeline points from one or more transcript chunks.\n"
        "Rewrite them into a polished final summary that is intuitive and detailed.\n"
        "Return ONLY a JSON array with objects containing 'timestamp' and 'point'.\n\n"
        "Final summary requirements:\n"
        "- Target 10 to 20 points based on content richness.\n"
        "- Preserve chronology and ensure smooth narrative flow.\n"
        "- Merge duplicates and remove vague points.\n"
        "- Keep concrete details (tools, steps, metrics, mistakes, outcomes).\n"
        "- Keep each point concise and useful for quick review.\n"
        "- Use timestamp format MM:SS or HH:MM:SS only.\n"
        "- No markdown, no headings, no prose outside JSON.\n\n"
        f"Draft points JSON:\n{json.dumps(points, ensure_ascii=True)}"
    )

    try:
        refined = _run_model([{"role": "user", "content": prompt}])
        refined = _cleanup_points(refined)
        if refined:
            return refined
    except RateLimitError:
        raise
    except SummarizationError as e:
        logger.warning(f"Refinement step failed, using chunk-level summary: {e}")

    return points


def summarize_transcript(chunks: list[dict]) -> list[dict]:
    """
    Summarize all transcript chunks and aggregate the results.
    
    Args:
        chunks: List of chunk dicts from the chunker utility.
        
    Returns:
        Aggregated list of summary points with timestamps.
    """
    all_points = []
    
    for i, chunk in enumerate(chunks):
        logger.info(f"Summarizing chunk {i + 1}/{len(chunks)}")
        
        try:
            points = summarize_chunk(chunk["text"])
            all_points.extend(points)
        except RateLimitError:
            raise
        except SummarizationError as e:
            logger.warning(f"Chunk {i + 1} summarization failed: {e}")
            # Continue with remaining chunks rather than failing entirely
            continue

    all_points = _cleanup_points(all_points)

    if chunks and not all_points:
        raise SummarizationError("No summary points generated from transcript")

    return refine_summary(all_points)
