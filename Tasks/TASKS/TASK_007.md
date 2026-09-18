# TASK_007: Ingestion API Endpoint

## 1. Objective

Expose the ingestion pipeline via a FastAPI endpoint to allow file uploads.

---

## 2. Architecture Mapping

*   **Architecture Section:** 3.2 (Container Diagram)
*   **Component:** `app/api/routes/ingest.py`
*   **PRD Section:** 5 (Backend Folder Structure)

---

## 3. Description

Create a POST endpoint `/ingest` that accepts file uploads, saves them temporarily, and triggers the ingestion pipeline.

---

## 4. Deliverables

*   `backend/app/api/routes/ingest.py`
*   Integration with `main.py` router.

---

## 5. Dependencies

### Hard Dependencies

*   TASK_006 (Ingestion Pipeline)
*   TASK_014 (API Routes setup - wait, TASK_014 is "API Routes (Query & Chat)". We can implement the endpoint file here but maybe need the main app structure from TASK_014 or TASK_001. Let's assume TASK_001 provided the app structure).

### Soft Dependencies

None.

---

## 6. Risks

*   **Security Risk:** Malicious file uploads. (Need basic validation).

---

## 7. Acceptance Criteria

*   `POST /api/v1/ingest` accepts a file.
*   Returns success message after processing.
*   Uploaded file content appears in Qdrant.

---

## 8. Definition of Done

*   [ ] Implementation complete
*   [ ] Manual test with Swagger UI (`/docs`)

---

## 9. Estimated Complexity

S
