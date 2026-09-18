# TASK_009: Reranking Module

## 1. Objective

Implement a reranking step to improve the precision of retrieved documents before passing them to the generator.

---

## 2. Architecture Mapping

*   **Architecture Section:** 3.2 (Retriever - Reranker component), 2.2 (Retrieval & Memory)
*   **Component:** `app/retrieval/reranker.py`
*   **PRD Section:** 2.2 (Reranking support)

---

## 3. Description

Develop the `Reranker` class. This uses a Cross-Encoder model (via Groq if available, or a lightweight local model like `ms-marco-TinyBERT-L-2-v2` or `bge-reranker-base`) to re-score the top-N results from the initial semantic search.

---

## 4. Deliverables

*   `backend/app/retrieval/reranker.py`
*   Unit tests.

---

## 5. Dependencies

### Hard Dependencies

*   TASK_008 (Retrieval Engine) - The reranker needs results to rerank.

### Soft Dependencies

None.

---

## 6. Risks

*   **Performance Risk:** Reranking adds latency.

---

## 7. Acceptance Criteria

*   `rerank(query: str, docs: List[Document])` returns a re-ordered list with new scores.
*   Top-K most relevant are effectively promoted.

---

## 8. Definition of Done

*   [x] Implementation complete
*   [x] Unit tests
*   [x] Verified improvement on test queries (manual check)

---

## 9. Estimated Complexity

M
