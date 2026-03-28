# YouTube Video Summarizer

AI-powered app that turns YouTube transcripts into structured, timestamped key points.

- Backend: FastAPI (Python)
- Frontend: React + Vite
- Model provider: OpenRouter (via OpenAI client SDK)

## Features

- Summarize a YouTube video from URL input
- Timestamped key-point output
- Clickable timestamps that open YouTube at the right moment
- Transcript chunking for long videos
- In-memory caching with TTL
- API rate limiting
- Dark and light theme toggle

## Project Structure

```text
Youtube-Summarizer/
  backend/
    main.py
    config.py
    models.py
    requirements.txt
    services/
      cache.py
      summarizer.py
      youtube.py
    utils/
      chunker.py
  frontend/
    index.html
    package.json
    vite.config.js
    src/
      App.jsx
      main.jsx
      index.css
      components/
      pages/
```

## Backend API

### GET /api/health

Returns API health.

Example response:

```json
{
  "status": "ok"
}
```

### POST /api/summarize

Summarizes a YouTube video.

Request:

```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

Response shape:

```json
{
  "title": "YouTube Video (dQw4w9WgXcQ)",
  "duration": "03:32",
  "summary": [
    {
      "timestamp": "00:12",
      "point": "Main idea introduced."
    }
  ],
  "video_id": "dQw4w9WgXcQ",
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

Notes:

- `title` is currently a generated placeholder based on `video_id`.
- Summaries are generated per transcript chunk and then merged.

## Error Responses

- `400`: Invalid YouTube URL format
- `403`: Video is private or restricted
- `422`: No transcript available for this video
- `429`: Service temporarily unavailable, try again later
- `500`: Failed to summarize video / unexpected server error

## Environment Variables

### backend/.env.example

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=google/gemma-3-4b-it:free
OPENROUTER_FALLBACK_MODELS=meta-llama/llama-3.3-70b-instruct:free,qwen/qwen3-coder:free,google/gemma-3-12b-it:free,mistralai/mistral-small-3.1-24b-instruct:free
FRONTEND_ORIGIN=http://localhost:5173
CACHE_TTL=86400
RATE_LIMIT=10/minute
SYSTEM_PROMPT=You are an expert content summarizer...
```

### frontend/.env.example

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Local Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- OpenRouter API key

### Backend (Windows PowerShell)

```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env and set OPENROUTER_API_KEY
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend (Windows PowerShell)

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev -- --host 127.0.0.1 --port 5173
```

Open:

- Frontend: http://127.0.0.1:5173
- Backend docs: http://127.0.0.1:8000/docs

## Quick Start

1. Start backend.
2. Start frontend.
3. Paste a valid YouTube URL.
4. Click Summarize.
5. Open timestamp cards to jump to exact moments in YouTube.

## Current Implementation Notes

- Transcript source: `youtube-transcript-api`
- Caching: in-memory singleton cache with TTL
- Rate limiting: `slowapi` per client IP
- CORS origin is controlled by `FRONTEND_ORIGIN`
- Frontend keeps summary state in memory (refreshing `/summary` resets view)

## Troubleshooting

- `Cannot connect to the server`
  - Ensure backend is running on `127.0.0.1:8000`
  - Ensure `VITE_API_BASE_URL` matches backend URL
- `No transcript available for this video`
  - Video may not have captions or transcript may be disabled
- `Service temporarily unavailable, try again later`
  - OpenRouter quota/rate limit reached

## Production Notes

- Move cache to Redis for multi-instance deployments
- Add real video metadata lookup for title
- Add persistent summary history (database)
- Keep secrets in `.env` and never commit API keys

## License and Usage

- Respect YouTube Terms of Service
- Summaries are AI-generated and may be imperfect

### API Design

| ✅ DO | ❌ DON'T |
|-------|----------|
| Version your endpoints (`/api/v1/summarize`) | Use unversioned root paths |
| Use consistent JSON response shapes | Return different structures per endpoint |
| Document all endpoints with FastAPI's auto-docs | Leave endpoints undocumented |
| Set CORS to allow only the frontend origin | Use `allow_origins=["*"]` in production |
| Rate limit by IP (10 req/min) | Allow unlimited requests |

### Git & Project

| ✅ DO | ❌ DON'T |
|-------|----------|
| Use `.env` for secrets with `.env.example` as template | Commit `.env` or API keys to the repo |
| Write descriptive commit messages | Use "fix", "update", "stuff" as commit messages |
| Keep `requirements.txt` and `package.json` up to date | Install packages without saving to dependency files |
| Add `.gitignore` for `node_modules/`, `venv/`, `.env`, `__pycache__/` | Track generated or environment-specific files |

### Security

| ✅ DO | ❌ DON'T |
|-------|----------|
| Store API keys in environment variables only | Expose API keys in frontend code |
| Sanitize all user input server-side | Trust client-side validation alone |
| Use HTTPS in production | Serve over plain HTTP |
| Implement rate limiting on all public endpoints | Leave endpoints open to abuse |
