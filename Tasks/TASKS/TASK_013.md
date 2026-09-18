# TASK_013: Memory Module (Short & Long Term)

## 1. Objective

Implement short-term session memory and long-term persistent memory using Qdrant.

---

## 2. Architecture Mapping

*   **Architecture Section:** 3.3 (Component Diagram - Memory), 2.2 (Retrieval & Memory)
*   **Component:** `app/memory/`
*   **PRD Section:** 2.2 (Short-term Memory, Long-term Memory)

---

## 3. Description

1.  **Short-term:** Manage the current conversation history in `AgentState`, ensuring it doesn't exceed token limits (FIFO or summarization).
2.  **Long-term:** Implement `LongTermMemory` class that can save summarized sessions to Qdrant and retrieve relevant past interactions based on the current query.

---

## 4. Deliverables

*   `backend/app/memory/short_term.py`
*   `backend/app/memory/long_term.py`
*   `backend/app/memory/summarizer.py`

---

## 5. Dependencies

### Hard Dependencies

*   TASK_004 (Qdrant Client)
*   TASK_012 (Agent Executor - needs to integration memory updates) - Wait, Agent Executor depends on Memory module to function fully, but we can implement Memory module logic independently first.

### Soft Dependencies

*   TASK_003 (Groq Client - for summarization)

---

## 6. Risks

*   **Performance:** Long-term memory retrieval adds latency.
*   **Cost:** Summarization uses tokens.

---

## 7. Acceptance Criteria

*   Short-term memory truncates or summarizes when limit reached.
*   Long-term memory successfully saves a session summary to Qdrant.
*   Relevant past sessions are retrieved for new queries.

---

## 8. Definition of Done

*   [ ] Implementation complete
*   [ ] Unit tests for summarizer
*   [ ] Integration test: Save -> Retrieve from Qdrant

---

## 9. Estimated Complexity

L
