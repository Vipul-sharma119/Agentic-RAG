# TASK_005: Embedding Service

## 1. Objective

Implement the service responsible for generating vector embeddings from text chunks.

---

## 2. Architecture Mapping

*   **Architecture Section:** 3.2 (Container Diagram), 4.2 (Offline Ingestion Flow)
*   **Component:** `app/retrieval/embedder.py`
*   **PRD Section:** 4.2 (Offline Ingestion Flow)

---

## 3. Description

Develop an `Embedder` class that uses the Groq client (or initially a local model if `gpt-oss-120b` doesn't support embeddings directly - wait, the PRD says to use `gpt-oss-120b` or a dedicated model. For stability, we might want to use a standard embedding model like `nomic-embed-text` via Groq or local `sentence-transformers`. Let's assume Groq for consistency, or local for cost/latency. Decision: Use a dedicated class that abstracts this, likely calling Groq's embedding endpoint or a local one).

*   *Constraint from PRD:* "Embedding: Generate vector embeddings for chunks (using gpt-oss-120b or dedicated embedding model)."

---

## 4. Deliverables

*   `backend/app/retrieval/embedder.py`
*   Unit tests.

---

## 5. Dependencies

### Hard Dependencies

*   TASK_003 (Groq Client) - if using Groq for embeddings.

### Soft Dependencies

None.

---

## 6. Risks

*   **Technical Risk:** Embedding dimension mismatch with Qdrant collection.

---

## 7. Acceptance Criteria

*   `embed_text(text: str)` returns a list of floats.
*   Embedding dimension matches configuration (e.g., 1024).

---

## 8. Definition of Done

*   [ ] Implementation complete
*   [ ] Unit tests passing
*   [ ] Verified dimension consistency

---

## 9. Estimated Complexity

S
