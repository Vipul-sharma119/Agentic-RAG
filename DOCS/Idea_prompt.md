```md
# 🚀 Production-Grade Agentic RAG System  
## (Qdrant + Groq GPT-OSS-120B + Modular Backend Architecture)

You are a **Senior AI Systems Architect and Production Backend Engineer**.

Your task is to design and implement a **fully production-grade Agentic RAG system** using:

- **Vector Database:** Qdrant (self-hosted/local)
- **LLM Provider:** Groq API
- **Model:** gpt-oss-120b
- **Backend Framework:** FastAPI (Python)
- **Architecture Pattern:** Agentic RAG (Planner + Tools + Memory + Validation)

---

# 🔴 MANDATORY RULE

You must:

1. **FIRST generate a complete, detailed PRD (Product Requirements Document).**
2. Only after the PRD is complete and coherent, proceed to implementation.
3. Do NOT generate toy code.
4. Do NOT collapse modules.
5. Do NOT simplify architecture.
6. Everything must be production-ready.

---

# PHASE 1 — PRODUCT REQUIREMENTS DOCUMENT (PRD)

Generate a complete, structured PRD with the following sections:

---

## 1️⃣ Executive Summary

- What system is being built
- Why Agentic RAG instead of traditional RAG
- Core system goals
- Explicit non-goals
- Key architectural principles

---

## 2️⃣ Functional Requirements

System must support:

- Multi-hop reasoning
- Iterative retrieval loop
- ReAct-style agent loop
- Query rewriting
- Hybrid-retrieval-ready architecture (even if initially dense-only)
- Metadata filtering
- Tool usage framework
- Short-term memory
- Long-term memory (stored in Qdrant)
- Context compression
- Reranking support
- Structured citations
- Answer validation step
- Iteration hard limits
- Token budget enforcement
- Config-driven behavior
- Evaluation hooks
- Streaming support

---

## 3️⃣ Non-Functional Requirements

Define:

- Latency targets
- Cost control mechanisms
- Scalability strategy
- Modularity constraints
- Security requirements
- Observability requirements
- Rate limiting
- Prompt injection resistance
- Fault tolerance
- Retry logic
- Circuit breaker design

---

## 4️⃣ System Architecture (Deep Design)

Clearly define:

### Online Query Flow

User  
→ API  
→ Router  
→ Planner  
→ Tool Execution Loop  
→ Retriever  
→ Memory  
→ Generator  
→ Validator  
→ Response

### Offline Ingestion Flow

Document Loader  
→ Cleaning  
→ Chunking  
→ Embedding  
→ Qdrant Upsert  

Define:

- Agent loop state schema
- Memory schema
- Retrieval schema
- Tool abstraction interface
- Failure handling logic
- Stop conditions

---

## 5️⃣ Backend Folder Structure (MANDATORY)

All backend code must live inside:

```

/backend

```

Inside backend:

```

backend/
│
├── app/
│ ├── main.py
│ ├── config.py
│ ├── dependencies.py
│ │
│ ├── api/
│ │ ├── routes/
│ │ │ ├── query.py
│ │ │ ├── ingest.py
│ │ │ └── health.py
│ │ └── schemas/
│ │ ├── request.py
│ │ └── response.py
│ │
│ ├── core/
│ │ ├── settings.py
│ │ ├── logging.py
│ │ ├── exceptions.py
│ │ └── security.py
│ │
│ ├── agent/
│ │ ├── planner.py
│ │ ├── executor.py
│ │ ├── state.py
│ │ ├── router.py
│ │ ├── validator.py
│ │ └── prompts.py
│ │
│ ├── retrieval/
│ │ ├── embedder.py
│ │ ├── qdrant_client.py
│ │ ├── retriever.py
│ │ ├── reranker.py
│ │ └── hybrid.py
│ │
│ ├── memory/
│ │ ├── short_term.py
│ │ ├── long_term.py
│ │ └── summarizer.py
│ │
│ ├── tools/
│ │ ├── base_tool.py
│ │ ├── retrieval_tool.py
│ │ └── memory_tool.py
│ │
│ ├── ingestion/
│ │ ├── loader.py
│ │ ├── chunker.py
│ │ ├── cleaner.py
│ │ └── pipeline.py
│ │
│ ├── llm/
│ │ ├── groq_client.py
│ │ ├── model_router.py
│ │ └── tokenizer.py
│ │
│ ├── evaluation/
│ │ ├── metrics.py
│ │ └── evaluator.py
│ │
│ └── utils/
│ ├── id_generator.py
│ └── helpers.py
│
├── tests/
├── .env.example
├── requirements.txt
└── README.md

```

This structure must be followed strictly.

---

# PHASE 2 — IMPLEMENTATION REQUIREMENTS

After PRD is completed, generate full production-ready code.

---

## Qdrant Integration

- Official Qdrant client
- Collection creation
- Schema validation
- Metadata payload support
- Filtered search
- Score threshold support
- Configurable:
  - vector size
  - top_k
  - score_threshold
  - collection name

---

## Groq GPT-OSS-120B Integration

Create:

```

llm/groq_client.py

```

Must support:

- Chat completion
- Streaming responses
- Tool-call compatible interface
- Temperature control
- Max tokens
- Retry logic
- Timeout handling
- Circuit breaker logic
- Environment-based API key

---

## Agent Loop

Implement strict ReAct-style loop:

```

for step in range(max_iterations):
thought = planner()
action = decide()
observation = tool_call()
update state
if termination_condition:
break

```

Constraints:

- Hard iteration limit
- Tool-call budget limit
- Token budget tracking
- Infinite loop protection
- Deterministic stop conditions

---

## Memory

### Short-Term Memory
- Pydantic-based state model
- Stores:
  - messages
  - retrieved docs
  - reasoning steps
  - iteration count

### Long-Term Memory
- Stored in Qdrant
- Conversation → summarize → embed → store
- Retrieval on new queries
- Metadata-tagged memory entries

---

## Validator

After generation:

- Groundedness check
- Citation validation
- Optional self-critique pass
- Re-retrieval trigger if low confidence

---

## Security

Must implement:

- Prompt injection mitigation
- Tool isolation
- Strict schema validation
- Input sanitization
- Rate limiting middleware
- Error boundary handling

---

## Logging & Observability

Structured logging must capture:

- Query
- Retrieval IDs
- Scores
- Tool calls
- Iteration count
- Token usage
- Latency
- Errors

---

## Evaluation Hooks

Provide pluggable:

- Faithfulness metric
- Retrieval recall metric
- Hallucination detection stub
- Cost tracking per request

---

# PHASE 3 — CODING STANDARDS

All code must:

- Follow PEP8
- Use full type hints
- Use Pydantic models
- Include docstrings
- Avoid global state
- Be dependency-injection friendly
- Be async where appropriate
- Clean separation of concerns
- Fully modular
- Production deployable

---

# PHASE 4 — README

Generate a complete README including:

- Setup instructions
- Environment variables
- Qdrant setup steps
- Groq setup steps
- Running instructions
- Example API requests
- Architecture explanation
- Extension guidelines
- Scaling recommendations

---

# FINAL CONSTRAINTS

- No toy implementation
- No collapsing of architecture
- No mixing responsibilities
- No skipping validation or safety
- System must be production-grade
- Code must be clean and modular
- Must start with PRD before code

Build this like it is going to production.

Start with PRD.
```
