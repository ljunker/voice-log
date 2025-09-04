# Voice Logs

Small Flask app to upload German audio logs, transcribe them with OpenAI, rewrite into a formal tone, and store both raw + formatted text in a database.  
Includes a simple web UI to upload files and view logs.

## Setup (local)

### Using pip

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export FLASK_ENV=development
export OPENAI_API_KEY=sk-...

flask --app app run --debug
```

### Using uv

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

export FLASK_ENV=development
export OPENAI_API_KEY=sk-...

flask --app app run --debug
```

Then open: http://127.0.0.1:5000

## Features
- Upload `.mp3`, `.m4a`, `.wav`, etc.
- Transcribes **German audio** via OpenAI Whisper / GPT
- Rewrites notes into a concise, formal German style
- Stores raw + formal logs in SQLite or Postgres
- Simple web UI for uploads and browsing logs

## Environment Variables
```env
OPENAI_API_KEY=sk-...
OPENAI_TRANSCRIBE_MODEL=whisper-1
OPENAI_TEXT_MODEL=gpt-4o-mini
UPLOAD_DIR=./uploads
DATABASE_URL=sqlite:///voice_logs.db
```

## Run with Docker (optional)
```bash
cp .env.example .env
docker compose up --build
```
Then open http://localhost:8000

