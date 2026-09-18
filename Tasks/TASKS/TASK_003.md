# TASK_003: Groq Client Implementation

## 1. Objective

Implement the client wrapper for interacting with the Groq API, supporting chat completion and tool calling.

---

## 2. Architecture Mapping

*   **Architecture Section:** 3.1 (System Context), 3.2 (Container Diagram)
*   **Component:** `app/llm/groq_client.py`
*   **PRD Section:** 4.1 (Online Query Flow), 2.2 (Data Schemas)

---

## 3. Description

Develop a robust Groq client that handles authentication, request formatting, response parsing, and error handling (retries, circuit breakers). It must support the `gpt-oss-120b` model and standard chat interfaces.

---

## 4. Deliverables

*   `backend/app/llm/groq_client.py`
*   Unit tests for the client.

---

## 5. Dependencies

### Hard Dependencies

*   TASK_002 (Settings & Logging)

### Soft Dependencies

None.

---

## 6. Risks

*   **Technical Risk:** API changes or rate limits from Groq.
*   **Integration Risk:** "gpt-oss-120b" model availability or behavior specificities.

---

## 7. Acceptance Criteria

*   Client can successfully send a user message and receive a text response.
*   Retries are triggered on 5xx errors or timeouts.
*   API Key is loaded safely from Settings.

---

## 8. Definition of Done

*   [ ] Implementation complete
*   [ ] Unit tests with mocked API responses
*   [ ] Integration test with real API (manual verification)

---

## 9. Estimated Complexity

M
