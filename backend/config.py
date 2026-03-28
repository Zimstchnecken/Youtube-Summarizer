import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemma-3-4b-it:free")
OPENROUTER_FALLBACK_MODELS = [
    model.strip()
    for model in os.getenv(
        "OPENROUTER_FALLBACK_MODELS",
        "meta-llama/llama-3.3-70b-instruct:free,qwen/qwen3-coder:free,google/gemma-3-12b-it:free,mistralai/mistral-small-3.1-24b-instruct:free",
    ).split(",")
    if model.strip()
]

def _compute_frontend_origins() -> list[str]:
    raw_origins = os.getenv("FRONTEND_ORIGINS", "")
    if raw_origins.strip():
        return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

    origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    origins = [origin]

    # Make local development resilient when switching between localhost and 127.0.0.1.
    if "localhost" in origin:
        origins.append(origin.replace("localhost", "127.0.0.1"))
    elif "127.0.0.1" in origin:
        origins.append(origin.replace("127.0.0.1", "localhost"))

    # Deduplicate while preserving order.
    deduped = []
    for item in origins:
        if item not in deduped:
            deduped.append(item)
    return deduped


FRONTEND_ORIGINS = _compute_frontend_origins()
CACHE_TTL = int(os.getenv("CACHE_TTL", "86400"))
RATE_LIMIT = os.getenv("RATE_LIMIT", "10/minute")

SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are an expert content summarizer. Your task is to extract the most important points from the following video transcript and present them as a concise, structured summary."
)
