# Product Requirements Document (PRD): Agentic RAG System

## 1. Project Overview
The **Agentic RAG System** is a sophisticated backend application designed to perform Retrieval-Augmented Generation (RAG) using an autonomous agentic approach. Unlike simple RAG systems that linearly retrieve and answer, this system employs an intelligent agent capable of planning, executing multi-step reasoning, and utilizing tools (like calculators and document retrieval) to answer complex user queries.

## 2. Technology Stack
- **Language**: Python 3.10+
- **Framework**: FastAPI (Async Web Framework)
- **Vector Database**: Qdrant (via `qdrant-client`)
- **LLM Provider**: Groq (Llama 3 70B via `groq` client)
- **Embedding Model**: `BAAI/bge-m3` (via Hugging Face Inference API)
- **PDF Processing**: `pypdf`
- **Text Splitting**: `langchain-text-splitters`
- **Testing**: `pytest`, `pytest-asyncio`

## 3. System Architecture
The system follows a modular architecture with clear separation of concerns:

### 3.1 High-Level Flow
1.  **Ingestion**: Documents (PDF/TXT) are uploaded -> Text is extracted -> Cleaned -> Chunked -> Embedded -> Stored in Qdrant.
2.  **Interaction**: User sends query -> Agent plans steps -> Agent executes loop (Call Tools / Reason) -> Agent constructs final answer.

### 3.2 Directory Structure
```
backend/
├── app/
│   ├── agent/          # Core Agent logic (Planning, State, Tools)
│   ├── api/            # FastAPI Routes (Chat, Ingestion)
│   ├── core/           # Config, Settings, Prompts
│   ├── ingestion/      # Document processing pipeline (Load, Clean, Chunk)
│   ├── llm/            # LLM Client wrappers (Groq)
│   ├── retrieval/      # RAG components (Embedder, Retriever, Reranker, Qdrant)
│   └── main.py         # Application Entrypoint
└── requirements.txt    # Dependencies
```

## 4. Core Components

### 4.1 Ingestion Pipeline
**Endpoint**: `POST /api/v1/ingest/`
**Files**: [app/ingestion/pipeline.py](file:///d:/STEP%202/Projects/Agentic%20RAG/backend/app/ingestion/pipeline.py), `loader.py`, `cleaner.py`, `chunker.py`
-   **Process**:
    1.  **Loader**: Reads file content (PDF or TXT).
    2.  **Cleaner**: Normalizes text (whitespace, etc.).
    3.  **Chunker**: Splits text into semantic chunks for embedding.
    4.  **Embedder**: Converts text chunks into vector embeddings using `BAAI/bge-m3`.
    5.  **Upsert**: Stores vectors + payload (content, metadata) in Qdrant.

### 4.2 Agentic Core
**Endpoint**: `POST /api/v1/chat/`
**Files**: [app/agent/agent.py](file:///d:/STEP%202/Projects/Agentic%20RAG/backend/app/agent/agent.py), [planner.py](file:///d:/STEP%202/Projects/Agentic%20RAG/backend/app/agent/planner.py), [state.py](file:///d:/STEP%202/Projects/Agentic%20RAG/backend/app/agent/state.py), [tools.py](file:///d:/STEP%202/Projects/Agentic%20RAG/backend/app/agent/tools.py)
-   **Planner**: Decomposes user queries into a sequence of actionable steps using an LLM.
-   **Agent Loop**: Iteratively executes the plan.
    -   **Decision Making**: Uses `AGENT_DECISION_PROMPT` to decide whether to use a tool, send a message, or finish.
    -   **Tools**:
        -   `retrieve_documents`: Searches Qdrant for relevant context. Includes a Reranking step for better precision.
        -   `calculator`: Performs arithmetic operations.
    -   **State Management**: Maintains conversation history and execution plan in `AgentState`.

### 4.3 Retrieval Layer
**Files**: `app/retrieval/`
-   **Embedder**: Wraps Hugging Face Inference Client. Uses `lru_cache` for singleton access.
-   **Retriever**: Performs vector similarity search in Qdrant.
-   **Reranker**: Re-scores retrieved documents to improve relevance before passing them to the context.

## 5. API Documentation

### 5.1 Ingestion API
**URL**: `/api/v1/ingest/`
**Method**: `POST`
**Body**: `multipart/form-data` -> [file](file:///d:/STEP%202/Projects/Agentic%20RAG/backend/app/api/routes/ingestion.py#12-67)
**Response**:
```json
{
  "message": "File ingested successfully",
  "filename": "document.pdf",
  "chunks_processed": 15
}
```

### 5.2 Chat API
**URL**: `/api/v1/chat/`
**Method**: `POST`
**Body**:
```json
{
  "query": "Calculate the revenue growth from 2022 to 2023 based on the report.",
  "session_id": "optional-session-id"
}
```
**Response**:
```json
{
  "query": "...",
  "answer": "The revenue growth is 15%.",
  "history": [...]
}
```

## 6. Configuration
Configuration is managed via [app/core/settings.py](file:///d:/STEP%202/Projects/Agentic%20RAG/backend/app/core/settings.py) using `pydantic-settings`.
**Key Environment Variables**:
-   `GROQ_API_KEY`: For LLM generation.
-   `HF_TOKEN`: For Embedding generation.
-   `QDRANT_HOST` / `QDRANT_PORT`: For Vector DB connection.
-   `QDRANT_API_KEY`: (Optional) authentication for Qdrant.

## 7. Setup & Deployment
1.  **Dependencies**: Install via `pip install -r requirements.txt`.
2.  **Environment**: Create [.env](file:///d:/STEP%202/Projects/Agentic%20RAG/backend/.env) file with required keys.
3.  **Qdrant**: Ensure Qdrant instance is running (Docker or Cloud).
4.  **Run**: `uvicorn app.main:app --reload`
