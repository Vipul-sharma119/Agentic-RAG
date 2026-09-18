# TASK_008: Retrieval Engine (Sem Search)

## 1. Objective

Implement the core retrieval logic that queries Qdrant to find relevant documents.

---

## 2. Architecture Mapping

*   **Architecture Section:** 3.3 (Component Diagram), 3.2 (Retriever)
*   **Component:** `app/retrieval/retriever.py`
*   **PRD Section:** 2.2 (Retrieval & Memory)

---

## 3. Description

Develop the `Retriever` class. It should take a query string, generate an embedding (using `Embedder`), and search Qdrant. It should support filtering by score threshold and top_k.

---

## 4. Deliverables

*   `backend/app/retrieval/retriever.py`
*   Unit tests.

---

## 5. Dependencies

### Hard Dependencies

*   TASK_004 (Qdrant Client)
*   TASK_005 (Embedder)

### Soft Dependencies

*   TASK_006 (Ingestion - to have data to test with, though not strictly code-dependent).

---

## 6. Risks

*   **Quality Risk:** Retrieval accuracy issues (too many irrelevant results).

---

## 7. Acceptance Criteria

*   `retrieve(query: str, k: int)` returns list of `Document` objects.
*   Results are sorted by relevance score.
*   Score filtering works.

---

## 8. Definition of Done

*   [x] Implementation complete
*   [x] Unit tests with mocked Qdrant
*   [x] Integration test with real data

---

## 9. Estimated Complexity

M
