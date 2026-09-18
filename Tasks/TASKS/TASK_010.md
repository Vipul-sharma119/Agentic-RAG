# TASK_010: Agent State & Planner

## 1. Objective

Define the state schema for the agent loop and implement the planning logic (Thought generation).

---

## 2. Architecture Mapping

*   **Architecture Section:** 3.3 (Component Diagram - Agent State, Planner), 5.2 (Application State)
*   **Component:** `app/agent/state.py`, `app/agent/planner.py`
*   **PRD Section:** 4.1 (Online Query Flow), 4.3 (Data Schemas)

---

## 3. Description

1.  Define `AgentState` Pydantic model (query, plan, history, context, scratchpad).
2.  Implement `Planner` which uses the LLM (via GroqClient) to generate a step-by-step plan or the next step based on the current state and user query.

---

## 4. Deliverables

*   `backend/app/agent/state.py`
*   `backend/app/agent/planner.py`
*   System prompts for planning.

---

## 5. Dependencies

### Hard Dependencies

*   TASK_003 (Groq Client)

### Soft Dependencies

*   TASK_016 (System Prompts - can include prompt in planner initially, then refactor).

---

## 6. Risks

*   **Quality Risk:** Planner gets stuck or hallucinates steps. (Requires prompt engineering).

---

## 7. Acceptance Criteria

*   `AgentState` captures all necessary context.
*   `Planner.plan(state)` returns a structured plan or next action.

---

## 8. Definition of Done

*   [x] Implementation complete
*   [x] Unit tests for state transition
*   [x] Unit tests for planner (mocked LLM)

---

## 9. Estimated Complexity

L
