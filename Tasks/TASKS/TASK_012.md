# TASK_012: Agent Executor (Loop)

## 1. Objective

Implement the main ReAct loop that orchestrates the Planner, Tools, and State updates.

---

## 2. Architecture Mapping

*   **Architecture Section:** 3.3 (Component Diagram - Executor), 4.1 (Online Query Flow), 4 (ADR-002: ReAct)
*   **Component:** `app/agent/executor.py`
*   **PRD Section:** 4.1 (Agent Loop), 2.4 (Control & Configuration)

---

## 3. Description

This is the heart of the system.
1.  Initialize `AgentState`.
2.  Loop:
    a. Call Planner (Thought).
    b. if "Final Answer", break.
    c. Select Tool (Action).
    d. Execute Tool (Observation).
    e. Update State (History + Scratchpad).
    f. Check Hard Limits (iterations).
3.  Return Final Answer.

---

## 4. Deliverables

*   `backend/app/agent/executor.py`

---

## 5. Dependencies

### Hard Dependencies

*   TASK_010 (Planner/State)
*   TASK_011 (Tools)

### Soft Dependencies

None.

---

## 6. Risks

*   **Logic Risk:** Infinite loops, malformed tool calls, losing context. This is the most complex logic.

---

## 7. Acceptance Criteria

*   Can solve a multi-step query (mocks allowed).
*   Correctly updates state at each step.
*   Respects iteration limits.
*   Handles tool errors gracefully.

---

## 8. Definition of Done

*   [ ] Implementation complete
*   [ ] Integration tests with mocked tools
*   [ ] E2E test with real tools (simple case)

---

## 9. Estimated Complexity

XL
