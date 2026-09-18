# TASK_015: Validator & Guardrails

## 1. Objective

Implement the post-generation validation step to ensure groundedness and safety.

---

## 2. Architecture Mapping

*   **Architecture Section:** 3.3 (Component Diagram - Validator), 2.3 (Answer Validation)
*   **Component:** `app/agent/validator.py`
*   **PRD Section:** 5.1 (Validator)

---

## 3. Description

Develop a `Validator` class that takes the generated answer and the retrieved context. It uses an LLM call to verify if the answer is supported by the context ("Groundedness Check"). If not, it can trigger a regeneration or flag the response.

---

## 4. Deliverables

*   `backend/app/agent/validator.py`
*   Validation prompts.

---

## 5. Dependencies

### Hard Dependencies

*   TASK_003 (Groq Client)

### Soft Dependencies

*   TASK_012 (Executor - to call validator at the end).

---

## 6. Risks

*   **Performance:** Adds latency as an extra API call.

---

## 7. Acceptance Criteria

*   `validate(answer, context)` returns a boolean or score.
*   Correctly identifies unsupported claims in test cases.

---

## 8. Definition of Done

*   [ ] Implementation complete
*   [ ] Unit tests with examples of hallucination vs grounded answers

---

## 9. Estimated Complexity

M
