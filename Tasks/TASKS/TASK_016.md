# TASK_016: System Prompts Management

## 1. Objective

Centralize and manage all system prompts, templates, and few-shot examples.

---

## 2. Architecture Mapping

*   **Architecture Section:** 3.3 (Agent Core), 6 (Security - Prompt Injection)
*   **Component:** `app/agent/prompts.py`
*   **PRD Section:** 5 (Backend Folder Structure)

---

## 3. Description

Create a dedicated module for prompt management. This allows for easier versioning, testing, and updating of prompts without changing code. Include standard system prompts for the Planner, Validator, and Tools.

---

## 4. Deliverables

*   `backend/app/agent/prompts.py`

---

## 5. Dependencies

### Hard Dependencies

None.

### Soft Dependencies

*   TASK_010 (Planner uses prompts)
*   TASK_015 (Validator uses prompts)

---

## 6. Risks

*   **Prompt Drift:** Prompts need to be adjusted if the model changes.

---

## 7. Acceptance Criteria

*   All hardcoded prompts in the codebase are moved to `prompts.py`.
*   Prompts are parameterized (e.g., using Jinja2 or f-strings).

---

## 8. Definition of Done

*   [ ] Implementation complete
*   [ ] Checked that no prompts remain in other files

---

## 9. Estimated Complexity

S
