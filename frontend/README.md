# Agentic RAG frontend

Next.js App Router UI for the FastAPI Agentic RAG backend.

## Features
- Streaming chat through POST /api/v1/chat/stream (SSE)
- Live planner steps, agent status updates, and tool-call activity
- PDF and TXT uploads through POST /api/v1/ingest/
- Conversation list and history via the backend sessions API
- Markdown and GitHub-flavoured Markdown rendering
- Dark/light theme, responsive layout, prompt suggestions, and API health indicator

## Requirements
- Node.js 20.9 or newer (required by Next.js 16)
- FastAPI backend running at http://localhost:8000

## Run locally
From the repository root:

    cd frontend
    npm install

Create .env.local (or copy .env.example):

    NEXT_PUBLIC_API_URL=http://localhost:8000

Start the development server:

    npm run dev

Open http://localhost:3000.

## API endpoints used
- GET /health
- POST /api/v1/chat/stream — JSON body: { "query": "...", "session_id": "..." }
- POST /api/v1/ingest/ — multipart field named file, PDF or TXT
- GET /api/v1/sessions/
- GET /api/v1/sessions/{session_id}

The backend session store is in-memory. Conversations disappear after a backend restart, and the session list is available only while that backend process is alive.
