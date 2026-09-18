# TASK_011: Tool Interface & Basic Tools

## 1. Objective

Define the standard `BaseTool` interface and implement the core tools (RetrievalTool, MemoryTool).

---

## 2. Architecture Mapping

*   **Architecture Section:** 3.3 (Component Diagram - ToolBox), 2.2 (Tool Usage Framework)
*   **Component:** `app/tools/`
*   **PRD Section:** 4.1 (Agent Loop - Tool Execution)

---

## 3. Description

1.  Create `BaseTool` abstract class (name, description, args_schema, run method).
2.  Implement `RetrievalTool` that wraps the `Retriever` (TASK_008).
3.  Implement `MemoryTool` (if needed for explicit memory access).
4.  Implement `CalculatorTool` (as a simple test tool).

---

## 4. Deliverables

*   `backend/app/tools/base_tool.py`
*   `backend/app/tools/retrieval_tool.py`
*   `backend/app/tools/calculator_tool.py`

---

## 5. Dependencies

### Hard Dependencies

*   TASK_010 (Agent State - tools might need state context) - Wait, usually tools are stateless or take clear inputs. Let's say TASK_008 is hard dependency for RetrievalTool.

### Soft Dependencies

*   TASK_008 (Retriever)

---

## 6. Risks

*   **Integration Risk:** LLM fails to call tools correctly (needs correct schema description).

---

## 7. Acceptance Criteria

*   All tools inherit from `BaseTool`.
*   `RetrievalTool` successfully calls the standard `Retriever`.
*   Tools have Pydantic schemas for their arguments.

---

## 8. Definition of Done

*   [ ] Implementation complete
*   [ ] Unit tests for each tool

---

## 9. Estimated Complexity

M
