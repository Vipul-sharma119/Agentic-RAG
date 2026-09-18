# Product Requirements Document (PRD) - Agentic RAG System

## 1️⃣ Executive Summary

### 1.1 Project Overview
We are building a **Production-Grade Agentic RAG System** designed to handle complex, multi-hop queries with high accuracy and reliability. Unlike traditional RAG systems that rely on a single retrieval step, this system employs an agentic architecture with planning, reasoning, tool usage, and memory capabilities.

### 1.2 Technology Stack
- **Vector Database:** Qdrant (Self-hosted/Local)
- **LLM Provider:** Groq API
- **Model:** `gpt-oss-120b` (accessible via Groq)
- **Backend Framework:** FastAPI (Python)
- **Architecture Pattern:** Agentic RAG (Planner + Tools + Memory + Validation)

### 1.3 Core Goals
- **Iterative Reasoning:** Enable the system to break down complex queries into sub-tasks and solve them step-by-step.
- **High Accuracy:** Use validation steps to ensure groundedness and reduce hallucinations.
- **Production Readiness:** Implement robust error handling, logging, observability, and security measures.
- **Scalability:** Design a modular architecture that can scale with increasing load and data volume.
- **Cost Efficiency:** Optimize token usage and leverage efficient models/APIs.

### 1.4 Non-Goals
- **Toy Implementation:** This is not a proof-of-concept; it must be production-ready.
- **Frontend Development:** The focus is strictly on the backend API and architecture.
- **Simplistic RAG:** We are avoiding basic "retrieve-then-generate" pipelines in favor of agentic workflows.

### 1.5 Key Architectural Principles
- **Modularity:** Components (Planner, Tools, Memory, etc.) are loosely coupled and easily interchangeable.
- **Observability:** Comprehensive logging and tracing to understand agent behavior.
- **Safety:** Strict input validation, output sanitization, and resource limits.

---

## 2️⃣ Functional Requirements

### 2.1 Core Capabilities
- **Multi-hop Reasoning:** The system must decompose complex user queries into logical steps.
- **Iterative Retrieval Loop:** Support for multiple retrieval passes based on intermediate findings.
- **ReAct-style Agent Loop:** Implement a Thought-Action-Observation loop for dynamic problem solving.
- **Query Rewriting:** Automatically refine user queries for better retrieval performance.
- **Tool Usage Framework:** A standardized interface for tools (Reception, Calculator, API calls, etc.).

### 2.2 Retrieval & Memory
- **Hybrid Retrieval:** Architecture should support both dense and sparse/keyword retrieval (initially dense-only).
- **Metadata Filtering:** Allow filtering search results based on document metadata.
- **Short-term Memory:** Maintain context within a session including messages, reasoning steps, and retrieved docs.
- **Long-term Memory:** Store summarized conversational history and user preferences in Qdrant.
- **Context Compression:** Summarize or select relevant context to fit within token limits.
- **Reranking:** Re-rank retrieved documents for higher relevance.

### 2.3 Output Generation
- **Structured Citations:** Responses must cite sources clearly.
- **Answer Validation:** An explicit step to verify the generated answer against retrieved evidence.
- **Streaming Support:** Stream tokens to the client for lower perceived latency.

### 2.4 Control & Configuration
- **Iteration Hard Limits:** Enforce maximum steps to prevent infinite loops (e.g., max 10 steps).
- **Token Budget Enforcement:** Track and limit token usage per request/session.
- **Config-driven Behavior:** System behavior (models, thresholds, limits) controlled via configuration files/env vars.
- **Evaluation Hooks:** Integration points for automated evaluation metrics (faithfulness, recall).

---

## 3️⃣ Non-Functional Requirements

### 3.1 Performance & Scalability
- **Latency:** Target sub-200ms initial token latency; end-to-end latency dependent on complexity (max 10s for complex queries).
- **Scalability:** Stateless backend service (FastAPI) horizontally scalable; Qdrant handles vector scale.
- **Circuit Breaker:** Implement circuit breakers for external API calls (Groq, Qdrant) to prevent cascading failures.
- **Rate Limiting:** Per-user and global rate limiting to protect resources.

### 3.2 Reliability & Fault Tolerance
- **Retry Logic:** Exponential backoff for transient failures (e.g., API timeouts).
- **Fault Tolerance:** Graceful degradation if non-essential services fail (e.g., logging).
- **Stop Conditions:** Deterministic stop conditions for the agent loop.

### 3.3 Security
- **Prompt Injection Resistance:** Use system prompts and input validation to mitigate injection attacks.
- **Tool Isolation:** Tools run in a controlled environment with strict permission boundaries.
- **Input Sanitization:** Sanitize all user inputs before processing.
- **API Security:** API Key authentication for backend access.

### 3.4 Observability
- **Structured Logging:** Log all key events (query, steps, tool calls, errors) with trace IDs.
- **Metrics:** Track request counts, latency, token usage, and error rates.
- **Cost Tracking:** Monitor token consumption and estimated costs per request.

---

## 4️⃣ System Architecture (Deep Design)

### 4.1 Online Query Flow
1.  **User Request:** User sends a query to the API.
2.  **API Layer:** Validates request, authenticates user.
3.  **Router:** Determines intent (Direct Answer vs. Agentic Workflow).
4.  **Planner:** Decomposes the query into a plan (if Agentic).
5.  **Agent Loop:**
    *   **Thought:** LLM analyzes current state and decides next step.
    *   **Action:** LLM selects a tool (e.g., `retrieve`, `calculator`).
    *   **Observation:** Tool executes and returns result.
    *   **Update:** State is updated with the observation.
6.  **Retriever:** Fetches relevant documents from Qdrant (if `retrieve` tool used).
7.  **Memory:** Fetches/Updates short-term and long-term memory.
8.  **Generator:** Synthesizes the final answer from accumulated context.
9.  **Validator:** Checks the answer for groundedness and safety.
10. **Response:** Helper formats and streams the response to the user.

### 4.2 Offline Ingestion Flow
1.  **Document Loader:** Load documents from source (PDF, TXT, etc.).
2.  **Cleaning:** Normalize text, remove noise.
3.  **Chunking:** Split text into semantic chunks (fixed-size or semantic splitting).
4.  **Embedding:** Generate vector embeddings for chunks (using `gpt-oss-120b` or dedicated embedding model).
5.  **Qdrant Upsert:** Store chunks with embeddings and metadata in Qdrant.

### 4.3 Data Schemas

#### Agent Loop State
```python
class AgentState(BaseModel):
    query: str
    plan: List[str]
    history: List[Message]
    current_step: int
    context: List[Document]
    scratchpad: str
```

#### Memory Schema (Qdrant Point)
```json
{
  "id": "uuid",
  "vector": [0.1, ...],
  "payload": {
    "content": "...",
    "role": "user|assistant",
    "timestamp": 1234567890,
    "session_id": "uuid"
  }
}
```

---

## 5️⃣ Backend Folder Structure (MANDATORY)

The project will follow this strict structure:

```
/backend
│
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Application configuration
│   ├── dependencies.py         # Dependency injection provider
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── query.py        # Query processing endpoints
│   │   │   ├── ingest.py       # Document ingestion endpoints
│   │   │   └── health.py       # Health check endpoints
│   │   └── schemas/
│   │       ├── request.py      # Pydantic request models
│   │       └── response.py     # Pydantic response models
│   │
│   ├── core/
│   │   ├── settings.py         # Environment settings
│   │   ├── logging.py          # Logging configuration
│   │   ├── exceptions.py       # Custom exception handling
│   │   └── security.py         # Authentication and security mechanisms
│   │
│   ├── agent/
│   │   ├── planner.py          # Planning logic
│   │   ├── executor.py         # Agent loop execution
│   │   ├── state.py            # State management
│   │   ├── router.py           # Intent routing
│   │   ├── validator.py        # Response validation
│   │   └── prompts.py          # System prompts and templates
│   │
│   ├── retrieval/
│   │   ├── embedder.py         # Embedding generation
│   │   ├── qdrant_client.py    # Qdrant interaction wrapper
│   │   ├── retriever.py        # Retrieval logic
│   │   ├── reranker.py         # Result reranking
│   │   └── hybrid.py           # Hybrid search implementation
│   │
│   ├── memory/
│   │   ├── short_term.py       # Session memory management
│   │   ├── long_term.py        # Persistent memory (Qdrant)
│   │   └── summarizer.py       # Context summarization
│   │
│   ├── tools/
│   │   ├── base_tool.py        # Tool interface/abstract class
│   │   ├── retrieval_tool.py   # Wrapper for retrieval as a tool
│   │   └── memory_tool.py      # Tools for memory interaction
│   │
│   ├── ingestion/
│   │   ├── loader.py           # Document loading
│   │   ├── chunker.py          # Text chunking
│   │   ├── cleaner.py          # Text cleaning
│   │   └── pipeline.py         # End-to-end ingestion pipeline
│   │
│   ├── llm/
│   │   ├── groq_client.py      # Groq API client
│   │   ├── model_router.py     # Logic for selecting models
│   │   └── tokenizer.py        # Token counting and management
│   │
│   ├── evaluation/
│   │   ├── metrics.py          # Evaluation metrics implementation
│   │   └── evaluator.py        # Evaluation runner
│   │
│   └── utils/
│       ├── id_generator.py     # ID generation utilities
│       └── helpers.py          # General helper functions
│
├── tests/                      # Unit and integration tests
├── .env.example                # Example environment variables
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## 6️⃣ Implementation Plan (Phase 2 Preview)

Following approval of this PRD, development will proceed in the following order:
1.  **Environment Setup:** Initialize repository, install dependencies, configure Qdrant and Groq.
2.  **Core Infrastructure:** Implement `settings`, `logging`, and `groq_client`.
3.  **Data Layer:** Implement `qdrant_client`, `embedder`, and `ingestion` pipeline.
4.  **Retrieval Engine:** Build `retriever` and `reranker`.
5.  **Agent Core:** Develop `planner`, `executor`, and `state`.
6.  **Tools & Memory:** Implement `tools` and `memory` modules.
7.  **API Layer:** Expose functionality via FastAPI routes.
8.  **Validation & QA:** Add `validator`, write tests, and perform end-to-end verification.
