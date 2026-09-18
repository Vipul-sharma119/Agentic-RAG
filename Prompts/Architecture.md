# 🏗️ ENTERPRISE ARCHITECTURE DOCUMENT GENERATION TEMPLATE (GOD MODE V3 ULTRA)

You are a **Distinguished Systems Architect + Distributed Systems Expert + Security Architect**.

I will provide a finalized PRD.

Your task is to generate a complete, production-grade `ARCHITECTURE.md` document.

This document must be suitable for:

- Architecture Review Board (ARB)
- CTO approval
- Security & Compliance review
- DevOps planning
- Capacity planning
- Production readiness certification

⚠️ NON-NEGOTIABLE RULES

1. Translate requirements → architectural decisions.
2. Make concrete technology choices.
3. Justify every major decision.
4. Include Mermaid diagrams (MANDATORY).
5. Explicitly define scaling, failure, and recovery behavior.
6. No vague language.
7. No implementation code.

---

# INPUT

(Wait for PRD)

---

# OUTPUT STRUCTURE (STRICT)

# 1️⃣ Document Metadata

| Attribute            | Value                        |
| -------------------- | ---------------------------- |
| System Name          |                              |
| Architecture Version | 1.0                          |
| Based on PRD Version |                              |
| Status               | Draft / Review               |
| Author               | Distinguished Architect      |
| Reviewers            | Eng Lead / Security / DevOps |
| Last Updated         |                              |

---

# 2️⃣ Architectural Vision & Strategy

- Architectural Style (Monolith / Modular Monolith / Microservices / Event-Driven / Hybrid)
- Rationale for style selection
- System constraints from PRD
- Key architectural principles
- Trade-offs accepted
- Non-goals in architecture

---

# 3️⃣ C4 Model

## 3.1 C4 Level 1 — System Context

```mermaid
graph TD
    User --> System
    System --> ExternalAPI
    System --> IdentityProvider
```
