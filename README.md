# 🤖 Agentic RAG

An **agentic Retrieval-Augmented Generation (RAG) system** that uses autonomous planning, multi-step reasoning, document retrieval, and tool execution to answer complex queries using user-provided knowledge.

## 🚀 Overview

Agentic RAG combines an AI agent with a modern RAG pipeline to go beyond simple question answering.

The agent can:

* Break complex queries into multiple actionable steps
* Retrieve relevant information from uploaded documents
* Use tools such as document retrieval and calculation
* Maintain conversation context across multiple turns
* Stream responses in real time

## ✨ Features

### 🧠 Agentic Reasoning

* **Autonomous Planning** — Decomposes complex queries into actionable steps
* **Multi-Step Execution** — Iteratively executes tools based on the generated plan
* **Conversation Memory** — Maintains context across multiple interactions
* **Tool Calling** — Dynamically selects and executes available tools

### 🔍 RAG Pipeline

* PDF and TXT document ingestion
* Semantic document chunking
* **BGE-M3** embeddings
* **Qdrant** vector similarity search
* **Cross-Encoder reranking** for improved relevance
* Context-aware retrieval for grounded responses

### 🛠️ Built-in Tools

* 📄 Document retrieval
* 🧮 Calculator
* 🔌 Extensible tool architecture for adding custom tools

### 💬 Chat Interface

* Real-time token streaming using **Server-Sent Events (SSE)**
* Markdown rendering for readable answers and code blocks
* Conversation history while the backend session store is running
* Dark and light themes
* Live agent plan, status and tool execution timeline
* Responsive chat and PDF/TXT upload interface

## 🏗️ Architecture

```text
┌──────────────────────────────────────────────┐
│              Next.js Frontend                │
│                                              │
│   Chat UI │ Streaming │ Zustand State       │
└──────────────────────┬───────────────────────┘
                       │
                 SSE / REST API
                       │
┌──────────────────────▼───────────────────────┐
│              FastAPI Backend                 │
│                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────┐ │
│  │ Agent Core │  │ RAG        │  │ LLM    │ │
│  │            │  │ Pipeline   │  │ Client │ │
│  │ Planner    │  │ Embedder   │  │ Groq   │ │
│  │ Tools      │  │ Retriever  │  │        │ │
│  │ State      │  │ Reranker   │  │        │ │
│  └────────────┘  └────────────┘  └────────┘ │
└──────────────────────┬───────────────────────┘
                       │
              ┌────────▼────────┐
              │     Qdrant      │
              │ Vector Database │
              └─────────────────┘
```

## 🧰 Technology Stack

### Backend

* **Python 3.10+**
* **FastAPI**
* **Groq — Llama 3.3 70B**
* **Hugging Face — BGE-M3**
* **Qdrant**
* **pypdf**
* **LangChain Text Splitters**
* **Pydantic**
* **pytest**

### Frontend

* **Next.js 16**
* **React 19**
* **TypeScript**
* **CSS design system**
* **lucide-react**
* **react-markdown**
* **remark-gfm**

### Infrastructure

* **Docker**
* **Server-Sent Events (SSE)**
* **REST APIs**

## 📁 Project Structure

```text
agentic-rag/
│
├── backend/
│   ├── app/
│   │   ├── agent/          # Planner, tools and agent state
│   │   ├── api/            # FastAPI routes and schemas
│   │   ├── core/           # Configuration and prompts
│   │   ├── ingestion/      # Document processing
│   │   ├── llm/            # LLM integration
│   │   ├── memory/         # Conversation memory
│   │   ├── retrieval/      # Embedding, retrieval and reranking
│   │   └── main.py
│   │
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── contexts/
│   ├── hooks/
│   ├── lib/
│   ├── store/
│   └── package.json
│
├── DOCS/
├── Knowledge/
├── Prompts/
└── README.md
```

## ⚡ Getting Started

### Prerequisites

Make sure you have:

* Python 3.10+
* Node.js 20.9+
* Docker
* Groq API key
* Hugging Face token

### 1. Clone

```bash
git clone https://github.com/Vipul-sharma119/agentic-rag.git
cd agentic-rag
```

### 2. Start Qdrant

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 3. Setup Backend

```bash
cd backend

python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env`:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile

HF_TOKEN=your_huggingface_token
EMBEDDING_MODEL=BAAI/bge-m3

QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_API_KEY=
QDRANT_COLLECTION=documents

LOG_LEVEL=INFO
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

### 4. Setup Frontend

Requires Node.js 20.9 or newer.

```bash
cd frontend
npm install
```

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start the frontend:

```bash
npm run dev
```

Frontend:

```text
http://localhost:3000
```

## 📚 Usage

### Upload Documents

1. Open **Knowledge library** in the frontend sidebar
2. Upload a PDF or TXT document
3. Wait for the API to process and index it
4. Ask questions about the document in Chat

### Ask Questions

Open the **Chat** page and submit a question.

The agent can:

```text
User Query
    ↓
Query Planning
    ↓
Tool Selection
    ↓
Document Retrieval
    ↓
Reranking
    ↓
Context Construction
    ↓
LLM Generation
    ↓
Streaming Response
```

### Example Queries

```text
"What is the revenue growth from 2022 to 2023?"

"Summarize the key findings from the uploaded report."

"Calculate 15% of the total revenue mentioned in the document."

"Explain the Bellman equation in reinforcement learning."
```

## 🔌 API

### Streaming Chat

```http
POST /api/v1/chat/stream
```

Example:

```json
{
  "query": "What is the revenue growth?",
  "session_id": "session-123"
}
```

The API streams agent events through **SSE**, including:

```text
plan
tool_call
token
done
```

### Document Ingestion

```http
POST /api/v1/ingest/
```

Accepts documents through `multipart/form-data`.

## 🧪 Testing

Run the complete backend test suite:

```bash
cd backend
pytest
```

Run specific tests:

```bash
pytest tests/test_agent.py
pytest tests/test_retrieval.py
```

Run with coverage:

```bash
pytest --cov=app tests/
```

## 📌 Key Highlights

* Agent-based **multi-step query planning**
* Retrieval-Augmented Generation with **BGE-M3**
* **Qdrant** vector database
* **Cross-Encoder reranking**
* Tool calling and execution
* FastAPI backend
* Next.js frontend
* Real-time **SSE streaming**
* Conversation memory
* Modular architecture for adding new tools

## 📄 License

This project is licensed under the **MIT License**.

See [LICENSE](LICENSE) for details.

---

Built with **Python, FastAPI, Next.js, Qdrant, and LLMs**.
