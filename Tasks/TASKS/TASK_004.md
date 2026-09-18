# TASK_004: Qdrant Client Wrapper

## 1. Objective

Implement the client wrapper for interacting with the Qdrant vector database, managing connection and collection initialization.

---

## 2. Architecture Mapping

*   **Architecture Section:** 3.2 (Container Diagram), 4 (ADR-001)
*   **Component:** `app/retrieval/qdrant_client.py`
*   **PRD Section:** 2.2 (Retrieval & Memory), 5.1 (Qdrant Schema)

---

## 3. Description

Develop a singleton client for Qdrant. It should ensure the required collection exists with the correct configuration (vector size, distance metric) on startup. It needs to support point upsertion and searching.

---

## 4. Deliverables

*   `backend/app/retrieval/qdrant_client.py`
*   Docker Compose service for Qdrant (or instructions for local install).

---

## 5. Dependencies

### Hard Dependencies

*   TASK_002 (Settings & Logging)

### Soft Dependencies

None.

---

## 6. Risks

*   **Operational Risk:** Connection failures or schema mismatches.

---

## 7. Acceptance Criteria

*   Can connect to a local Qdrant instance.
*   Automatically creates the collection if it doesn't exist.
*   Can inspect collection info.

---

## 8. Definition of Done

*   [ ] Implementation complete
*   [ ] Unit/Integration tests for connection and collection creation
*   [ ] Qdrant running locally

---

## 9. Estimated Complexity

M
