# TASK_014: API Routes (Query & Chat)

## 1. Objective

Implement the public-facing API endpoints for the Agentic RAG system.

---

## 2. Architecture Mapping

*   **Architecture Section:** 3.2 (Container Diagram - Router/API)
*   **Component:** `app/api/routes/query.py`
*   **PRD Section:** 4.1 (Online Query Flow), 5 (Backend Folder Structure)

---

## 3. Description

Create `/api/v1/chat` and `/api/v1/query` endpoints.
1.  **Chat:** Standard chat completion interface (compat with frontend).
2.  **Query:** Detailed RAG query endpoint that returns reasoning steps and citations.
3.  Implement Streaming response support.

---

## 4. Deliverables

*   `backend/app/api/routes/query.py`
*   Pydantic Schemas (`Request`, `Response`).
*   Integration with `Executor`.

---

## 5. Dependencies

### Hard Dependencies

*   TASK_012 (Agent Executor)
*   TASK_013 (Memory - optionally)

### Soft Dependencies

None.

---

## 6. Risks

*   **UX Risk:** Latency is too high for real-time chat. (Streaming is critical).

---

## 7. Acceptance Criteria

*   `POST /chat` returns valid response.
*   Response includes `citations` field.
*   Streaming works.

---

## 8. Definition of Done

*   [ ] Implementation complete
*   [ ] Verified with curl/Postman
*   [ ] Unit tests for route logic

---

## 9. Estimated Complexity

M
