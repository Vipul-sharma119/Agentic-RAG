# 🤖 Agentic RAG System

A sophisticated **Retrieval-Augmented Generation (RAG)** system powered by autonomous agents that can plan, reason, and execute multi-step tasks to answer complex queries.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16.1+-black.svg)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

### 🧠 Intelligent Agent System
- **Autonomous Planning**: Decomposes complex queries into actionable steps
- **Multi-Step Reasoning**: Executes plans with iterative tool usage
- **Context-Aware**: Maintains conversation history for coherent interactions

### 🔍 Advanced RAG Pipeline
- **Document Ingestion**: Supports PDF and TXT files
- **Semantic Chunking**: Intelligent text splitting for optimal retrieval
- **Vector Search**: Powered by Qdrant for fast similarity search
- **Reranking**: Improves relevance of retrieved documents

### 💬 Modern Chat Interface
- **Real-Time Streaming**: ChatGPT-style token-by-token responses
- **Rich Formatting**: Markdown, LaTeX math, code syntax highlighting
- **Message Actions**: Edit, retry, regenerate, copy, and delete messages
- **Dark/Light Mode**: Beautiful themes with smooth transitions
- **Execution Timeline**: Visual feedback of agent's reasoning process

### 🛠️ Built-in Tools
- **Document Retrieval**: Searches knowledge base for relevant context
- **Calculator**: Performs arithmetic operations
- **Extensible**: Easy to add custom tools

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Chat UI      │  │ Streaming    │  │ State Mgmt   │      │
│  │ Components   │  │ Controller   │  │ (Zustand)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↕ SSE / REST API
┌─────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Agent Core   │  │ RAG Pipeline │  │ LLM Client   │      │
│  │ - Planner    │  │ - Embedder   │  │ (Groq)       │      │
│  │ - Tools      │  │ - Retriever  │  └──────────────┘      │
│  │ - State      │  │ - Reranker   │                         │
│  └──────────────┘  └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    Vector Database (Qdrant)                  │
│              Document Embeddings + Metadata                  │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **Qdrant** (Docker or Cloud)
- **API Keys**:
  - Groq API Key ([Get it here](https://console.groq.com/))
  - Hugging Face Token ([Get it here](https://huggingface.co/settings/tokens))

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/agentic-rag.git
cd agentic-rag
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your API keys
```

**Backend `.env` Configuration:**
```env
# LLM Provider
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Embeddings
HF_TOKEN=your_huggingface_token_here
EMBEDDING_MODEL=BAAI/bge-m3

# Vector Database
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_API_KEY=  # Optional
QDRANT_COLLECTION=documents

# Application
LOG_LEVEL=INFO
```

**Start Qdrant (Docker):**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**Run Backend:**
```bash
uvicorn app.main:app --reload
# Backend runs on http://localhost:8000
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.local.example .env.local
# Edit .env.local with backend URL
```

**Frontend `.env.local` Configuration:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Run Frontend:**
```bash
npm run dev
# Frontend runs on http://localhost:3000
```

### 4. Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs

## 📚 Usage

### Ingesting Documents

1. Navigate to the **Ingest** page
2. Upload PDF or TXT files
3. Wait for processing to complete
4. Documents are now searchable

### Chatting with the Agent

1. Go to the **Chat** page
2. Type your question
3. Watch the agent:
   - Generate a plan
   - Execute tools (retrieve documents, calculate)
   - Stream the response in real-time

### Example Queries

```
"What is the revenue growth from 2022 to 2023?"
"Summarize the key findings from the uploaded report"
"Calculate 15% of the total revenue mentioned in the document"
"Explain the Bellman equation in reinforcement learning"
```

## 🎨 Features in Detail

### Message Context Menu
Right-click any message to:
- ✏️ **Edit** user messages and regenerate responses
- 🔁 **Retry** failed or unsatisfactory responses
- 📋 **Copy** message content to clipboard
- 🗑️ **Delete** messages from conversation

### LaTeX Math Rendering
Supports beautiful mathematical notation:
- **Inline**: `$E = mc^2$` → E = mc²
- **Block**: `$$\sum_{i=1}^{n} x_i$$` → Centered equation

### Code Syntax Highlighting
Automatic syntax highlighting for code blocks in multiple languages.

### Dark/Light Mode
Toggle between themes with smooth transitions.

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (async Python web framework)
- **LLM**: Groq (Llama 3.3 70B)
- **Embeddings**: BAAI/bge-m3 via Hugging Face
- **Vector DB**: Qdrant
- **Document Processing**: pypdf, langchain-text-splitters
- **Testing**: pytest, pytest-asyncio

### Frontend
- **Framework**: Next.js 16 (React 19)
- **Styling**: Tailwind CSS 4
- **State Management**: Zustand
- **Animations**: Framer Motion
- **Markdown**: react-markdown with KaTeX
- **Code Highlighting**: react-syntax-highlighter
- **UI Components**: Radix UI + shadcn/ui

## 📁 Project Structure

```
agentic-rag/
├── backend/
│   ├── app/
│   │   ├── agent/          # Agent logic (planner, tools, state)
│   │   ├── api/            # FastAPI routes
│   │   │   ├── routes/     # Chat, ingestion, sessions
│   │   │   └── schemas/    # Pydantic models
│   │   ├── core/           # Config, settings, prompts
│   │   ├── ingestion/      # Document processing pipeline
│   │   ├── llm/            # LLM client (Groq)
│   │   ├── memory/         # Conversation memory
│   │   ├── retrieval/      # RAG components (embedder, retriever, reranker)
│   │   └── main.py         # Application entry point
│   ├── tests/              # Backend tests
│   └── requirements.txt
│
├── frontend/
│   ├── app/                # Next.js app directory
│   ├── components/         # React components
│   │   ├── chat/          # Chat UI components
│   │   └── ui/            # Reusable UI components
│   ├── contexts/          # React contexts (theme)
│   ├── hooks/             # Custom React hooks
│   ├── lib/               # Utilities and API client
│   ├── store/             # Zustand state management
│   └── package.json
│
├── DOCS/                  # Documentation
├── Knowledge/             # Knowledge base
├── Prompts/              # Prompt templates
└── README.md
```

## 🔧 Configuration

### Backend Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GROQ_API_KEY` | Groq API key for LLM | Yes | - |
| `GROQ_MODEL` | Groq model name | No | `llama-3.3-70b-versatile` |
| `HF_TOKEN` | Hugging Face token | Yes | - |
| `EMBEDDING_MODEL` | Embedding model | No | `BAAI/bge-m3` |
| `QDRANT_HOST` | Qdrant host | No | `localhost` |
| `QDRANT_PORT` | Qdrant port | No | `6333` |
| `QDRANT_API_KEY` | Qdrant API key | No | - |
| `QDRANT_COLLECTION` | Collection name | No | `documents` |
| `LOG_LEVEL` | Logging level | No | `INFO` |

### Frontend Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | Yes | `http://localhost:8000` |

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Run Specific Tests

```bash
# Test agent
pytest tests/test_agent.py

# Test retrieval
pytest tests/test_retrieval.py

# Test with coverage
pytest --cov=app tests/
```

## 📊 API Documentation

### Chat API (Streaming)

**Endpoint**: `POST /api/v1/chat/stream`

**Request:**
```json
{
  "query": "What is the revenue growth?",
  "session_id": "session-123"
}
```

**Response**: Server-Sent Events (SSE)
```
event: plan
data: {"steps": ["Retrieve documents", "Calculate growth"]}

event: tool_call
data: {"tool": "retrieve_documents", "args": {...}}

event: token
data: {"content": "The"}

event: token
data: {"content": " revenue"}

event: done
data: {"answer": "The revenue growth is 15%", "total_ms": 2500}
```

### Ingestion API

**Endpoint**: `POST /api/v1/ingest/`

**Request**: `multipart/form-data`
```
file: document.pdf
```

**Response:**
```json
{
  "message": "File ingested successfully",
  "filename": "document.pdf",
  "chunks_processed": 42
}
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq** for fast LLM inference
- **Qdrant** for vector database
- **Hugging Face** for embeddings
- **FastAPI** for the backend framework
- **Next.js** for the frontend framework
- **shadcn/ui** for beautiful UI components

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using FastAPI, Next.js, and AI**
