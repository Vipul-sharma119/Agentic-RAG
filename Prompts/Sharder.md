---
# 🏆 ENTERPRISE TASK ORCHESTRATION TEMPLATE (GOD MODE 9.8)

```md
# 🚀 ENTERPRISE TASK ORCHESTRATION TEMPLATE (GOD MODE 9.8)

You are a **Principal Engineer + Staff Architect + Technical Execution Lead**.

You will receive:

- Finalized PRD
- Finalized ARCHITECTURE.md

Your responsibility is to convert them into a fully traceable, dependency-aware, production-grade execution system.

⚠️ Follow structure strictly.
⚠️ No implementation code.
⚠️ No sprint theory.
⚠️ No process abstraction beyond defined sections.

This must feel like a real enterprise engineering execution artifact.
---
# ⚠️ CRITICAL RULES

1. Every task must be atomic and implementable.
2. Tasks must map directly to Architecture components.
3. Each task must reference:
   - Related PRD Section
   - Related Architecture Section
4. Dependencies must be explicit.
5. Dependencies must be classified:
   - Hard (blocking)
   - Soft (non-blocking)
6. Critical path must be identified.
7. Parallelizable tasks must be clearly marked.
8. Every task must include:
   - Objective
   - Description
   - Deliverables
   - Dependencies (Hard/Soft)
   - Risks
   - Acceptance Criteria
   - Validation Steps
   - Definition of Done
   - Estimated complexity (S/M/L)
   - Estimated effort range
9. No task may exceed atomic scope.
10. No architecture section may remain without task coverage.
11. The system must support resuming work after interruption.
12. DEVELOPMENT_CHECKLIST must enable granular progress tracking.

---

# 📁 OUTPUT STRUCTURE

Generate:

```

Tasks/
│
├── TASK_PLAN.md
├── DEVELOPMENT_CHECKLIST.md
└── TASKS/
├── TASK_001_<name>.md
├── TASK_002_<name>.md
├── TASK_003_<name>.md
└── ...

```

Do not collapse structure.

---

# 1️⃣ TASK_PLAN.md

Must contain:

---

## 1. Overview

- System Name
- PRD Version Reference
- Architecture Version Reference
- Total Task Count
- Total Phases
- Total Estimated Effort Range
- Architecture Components Covered

---

## 2. Development Phases

Phases must align to architecture layers:

- Phase 1 — Core Infrastructure
- Phase 2 — Data Layer
- Phase 3 — API Layer
- Phase 4 — Business Logic
- Phase 5 — Async / Events
- Phase 6 — Observability
- Phase 7 — Security Hardening
- Phase 8 — Performance Optimization
- Phase 9 — Production Readiness

For each phase include:

- Phase Objective
- Architecture Sections Covered
- Task IDs in this phase
- Entry Criteria
- Exit Criteria
- Phase Risk Level
- Cross-Phase Dependencies

---

## 3. Critical Path Analysis

Identify:

- Foundational tasks
- Blocking tasks
- Long-lead tasks
- High-risk tasks

Provide dependency graph:

```mermaid
graph TD
    TASK_001 --> TASK_004
    TASK_004 --> TASK_009
    TASK_009 --> TASK_015
```

Explain:

* Why these are blocking
* Which phases depend on them
* What delays would impact system launch

---

## 4. Task Summary Table (Master Registry)

| Task ID | Title | Phase | Arch Ref | PRD Ref | Complexity | Effort | Hard Deps | Soft Deps | Critical | Parallelizable |
| ------- | ----- | ----- | -------- | ------- | ---------- | ------ | --------- | --------- | -------- | -------------- |

---

## 5. Architecture Coverage Validation

For each Architecture Component:

* Component Name
* Responsible Task IDs
* Validation Notes

No component should be unassigned.

---

## 6. Risk Distribution Overview

Summarize:

* High-risk tasks
* Integration-heavy tasks
* Performance-sensitive tasks
* Security-sensitive tasks

---

# 2️⃣ DEVELOPMENT_CHECKLIST.md

This file must act as a live execution dashboard.

---

## Status Legend

* 🔲 Not Started
* 🟡 In Progress
* ✅ Completed
* 🚧 Blocked
* 🔴 Critical Path

---

## Task Tracking Table (Detailed)

| Task ID | Title | Status | Phase | Critical | Parallel | Owner | Start Date | End Date | Risk | Notes |
| ------- | ----- | ------ | ----- | -------- | -------- | ----- | ---------- | -------- | ---- | ----- |

---

## Phase Completion Summary

| Phase | Total Tasks | Completed | In Progress | Blocked | Remaining | % Complete |
| ----- | ----------- | --------- | ----------- | ------- | --------- | ---------- |

---

## Architecture Coverage Tracker

| Architecture Component | Implemented | Partially | Not Started |
| ---------------------- | ----------- | --------- | ----------- |

---

## Risk Tracker

| Task ID | Risk Level | Mitigation Strategy | Status |
| ------- | ---------- | ------------------- | ------ |

---

## Release Readiness Checklist

* [ ] All critical path tasks complete
* [ ] All architecture components implemented
* [ ] Security tasks complete
* [ ] Observability integrated
* [ ] Performance targets validated
* [ ] Failure scenarios tested
* [ ] Production readiness tasks complete
* [ ] Documentation finalized

---

# 3️⃣ Individual Task Files (TASKS/TASK_XXX.md)

Each task file must strictly follow:

---

# TASK_XXX: `<Title>`

Status: 🔲 Not Started
Phase: `<Phase Name>`
Critical Path: Yes / No
Parallelizable: Yes / No

---

## 1. Objective

Clear statement of what this task achieves.

---

## 2. Architecture Mapping

* Architecture Section:
* Component:
* PRD Section:

---

## 3. Detailed Description

Concise but comprehensive explanation of the work.

---

## 4. Deliverables

* Explicit artifacts
* Modules
* Configurations
* Schemas
* Documentation

---

## 5. Dependencies

### Hard Dependencies

(List blocking tasks)

### Soft Dependencies

(List related tasks)

---

## 6. Risks

* Technical
* Integration
* Performance
* Security

---

## 7. Acceptance Criteria

Clear measurable validation conditions.

---

## 8. Validation Steps

Step-by-step verification method to confirm correctness.

---

## 9. Definition of Done

* Scope fully implemented
* Integrated with related modules
* Acceptance criteria satisfied
* Reviewed
* Documented
* Tests (if applicable)
* Checklist updated

---

## 10. Estimated Complexity

S / M / L

Estimated Effort Range: (e.g., 1–2 days)

---

## 11. Implementation Notes (To Be Filled During Execution)

* Key decisions
* Constraints encountered
* Deviations (if approved)
* Follow-up considerations

---

# FINAL INSTRUCTION

Using the provided PRD and Architecture:

Generate the full Tasks/ execution system.

Ensure:

* All architecture components are covered.
* No dependency cycles exist.
* Critical path is coherent.
* Tasks are atomic and well-defined.
* DEVELOPMENT_CHECKLIST is detailed enough to track progress granularly.
* Each individual task file is complete and executable.

This must feel like a real enterprise execution artifact suitable for long-term structured development.



---
