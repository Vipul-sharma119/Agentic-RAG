# TASK_006: Ingestion Pipeline (Loader/Chunker)

## 1. Objective

Implement the document loading, cleaning, chunking, and ingestion logic.

---

## 2. Architecture Mapping

*   **Architecture Section:** 4.2 (Offline Ingestion Flow), 3.2 (Container Diagram)
*   **Component:** `app/ingestion/` (`loader.py`, `chunker.py`, `cleaner.py`, `pipeline.py`)
*   **PRD Section:** 4.2 (Offline Ingestion Flow)

---

## 3. Description

This is a large task involving the "ETL" part of RAG.
1.  **Loader:** Read files (PDF, TXT) from a directory or upload.
2.  **Cleaner:** Remove whitespace, normalize text.
3.  **Chunker:** Split text into overlapping segments (e.g., recursive character splitter).
4.  **Pipeline:** Orchestrate Load -> Clean -> Chunk -> Embed -> Qdrant Upsert.

---

## 4. Deliverables

*   `backend/app/ingestion/loader.py`
*   `backend/app/ingestion/cleaner.py`
*   `backend/app/ingestion/chunker.py`
*   `backend/app/ingestion/pipeline.py`
*   Modules for processing PDF/Text.

---

## 5. Dependencies

### Hard Dependencies

*   TASK_004 (Qdrant Client)
*   TASK_005 (Embedder)

### Soft Dependencies

None.

---

## 6. Risks

*   **Result Risk:** Poor chunking leads to poor retrieval quality.
*   **Performance Risk:** Slow ingestion for large files.

---

## 7. Acceptance Criteria

*   Can take a PDF file and populate the Qdrant collection with chunks.
*   Chunks contain correct metadata (source, page number).
*   Chunk overlap is respected.

---

## 8. Definition of Done

*   [ ] Implementation complete
*   [ ] Unit tests for Chunker
*   [ ] Integration test: File -> Qdrant
*   [ ] Tested with sample PDF

---

## 9. Estimated Complexity

L
