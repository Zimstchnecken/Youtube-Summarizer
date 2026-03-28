# YouTube Summarizer

This app helps you understand a YouTube video quickly.

You paste a video link, then the app gives you:
- a short timeline
- key points
- clickable timestamps

## What You Need

You only need 3 things installed:
1. Python (version 3.10 or newer)
2. Node.js (version 18 or newer)
3. An OpenRouter API key

## What This App Does

1. Reads a YouTube video's subtitles/transcript
2. Sends the transcript to an AI model
3. Returns a clear summary with timestamps

## Step-by-Step Setup (Windows)

Open PowerShell in this project folder and follow the steps below.

### 1. Start the backend (server)

```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Now open `.env` and put your real OpenRouter API key here:

```env
OPENROUTER_API_KEY=your_real_key_here
```

Then run:

```powershell
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Keep this terminal open.

### 2. Start the frontend (website)

Open a second PowerShell window:

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev -- --host 127.0.0.1 --port 5173
```

Keep this terminal open too.

### 3. Use the app

Open this in your browser:

http://127.0.0.1:5173

Paste a YouTube link and click **Summarize**.

## If Something Goes Wrong

### Error: Cannot connect to the server

Usually this means backend is not running.

Check:
1. Backend terminal is still open
2. Backend is running on `127.0.0.1:8000`
3. Frontend is running on `127.0.0.1:5173`

### Error: No transcript available for this video

This video probably has no subtitles/transcript, or the transcript is disabled.

Try a different video.

### Error: Service temporarily unavailable

The AI provider is rate-limited right now.

Wait a little and try again.

## Common Questions

### Do I need to pay?

You can use free OpenRouter models, but they may have limits.

### Can I summarize any YouTube video?

Only videos with accessible transcript/subtitles can be summarized.

### Is the summary always perfect?

No. AI summaries can make mistakes. Always verify important details.

## Important Files

- `backend/.env` - your secret API settings
- `frontend/.env` - frontend app settings
- `backend/main.py` - backend API
- `backend/services/summarizer.py` - summary logic

Do not upload `backend/.env` to public GitHub.

## Quick Start (Very Short Version)

1. Run backend on port `8000`
2. Run frontend on port `5173`
3. Open `http://127.0.0.1:5173`
4. Paste link and summarize

## Notes

- The app is for learning and productivity.
- Respect YouTube terms of use.
- AI output can be wrong sometimes.
