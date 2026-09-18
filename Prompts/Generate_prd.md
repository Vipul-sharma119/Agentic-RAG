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
