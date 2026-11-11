# Implementation Roadmap

## Mission

Build a broad catalogue of 500 AI agent projects and patterns, while earning completeness through working implementations rather than counting folders. The 500-entry catalogue is now established; implementation and verification remain separate milestones.

## Catalogue baseline

- [x] Define 500 distinct project specifications across 10 tracks.
- [x] Publish human-readable and machine-readable catalogues.
- [x] Add track-level entry points and implementation expectations.
- [ ] Implement and verify projects in priority order.

See [PROJECT_CATALOG.md](PROJECT_CATALOG.md), [projects.json](../catalogue/projects.json), and [projects.csv](../catalogue/projects.csv).

## Priority tracks

| Priority | Track | Scope |
|---|---|---|
| P0 | Foundations | LLM client, structured output, tool calling, loops, state, memory, retries |
| P0 | RAG and data | ingestion, chunking, embeddings, retrieval, reranking, citations, evaluation |
| P0 | MCP | servers, clients, discovery, multiple servers, authorization, resilience |
| P0 | Orchestration | graph workflows, routing, planner/executor, supervisor, human-in-loop |
| P0 | Security and evaluation | threat testing, policy enforcement, groundedness, regression, observability |
| P1 | Developer agents | code review, debugging, tests, docs, issue triage, repository agent |
| P1 | DevOps agents | logs, incidents, Kubernetes, cloud inventory, deployment review |
| P1 | Domain agents | support, research, analytics, logistics, education, agriculture, healthcare admin |
| P2 | Advanced agents | browser, voice, long-running tasks, multimodal workflows |
| P2 | Research and productivity | evidence gathering, synthesis, personal and team knowledge workflows |

## Reference audit: initial structural snapshot

Reference: [ashishpatel26/500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects), inspected on 2026-11-12. The initial recursive tree contained 179 entries: 145 files and 34 directories. Under `agents/`, there were 21 numbered project folders. All 21 had a README, a code file, and a dependency/configuration file. A filename-level scan found one project folder with a test-like filename and no Docker files in those 21 folders.

This was a structural scan only; it does not establish whether upstream projects run or are high/low quality. No source is copied by default. Ideas are independently scoped and implemented, with third-party licence and attribution checks where reuse occurs.

## Existing implementations

- [x] AG-001 Tool-calling agent: bounded loop, allowlisted tools, validation, Ollama adapter (verification pending).
- [x] AG-002 Structured-output agent: schema-constrained generation and strict Pydantic validation (verification pending).
- [x] AG-003 Prompt boundary demo: trusted system/developer messages, untrusted user framing, and provider role mapping (verification pending).
- [x] AG-004 Conversation history manager: bounded session-scoped history, complete-turn trimming, and isolation (verification pending).
- [x] AG-005 Token budget estimator: pluggable token counter, output/safety reservation, mandatory context protection, and priority-based admission (verification pending).
- [x] AG-006 Context-window truncation strategy: mandatory system/current-user preservation, complete-turn integrity, newest-first retention, and explicit overflow (verification pending).
- [x] AG-007 Evidence-backed entity extraction agent: typed entity schema, exact source-substring evidence checks, duplicate rejection, and explicit validation failures (verification pending).
- [x] AG-008 Schema repair and retry agent: strict Pydantic validation, bounded feedback, configurable repair attempts, and explicit exhaustion handling (verification pending).
- [x] AG-009 Tool-calling calculator: Ollama tool selection, strict argument validation, restricted AST evaluation with Decimal, and bounded execution (verification pending).
- [ ] Run AG-001 and AG-002 in clean Python 3.12 environments and verify Ollama integration; run AG-003 tests and CLI locally; run AG-004 tests and history demo; run AG-005 tests and budget demo; run AG-006 tests and truncation demo; run AG-007 tests and entity extraction demo; run AG-008 tests and repair/retry demo; run AG-009 calculator tests and Ollama tool-call demo.

## Delivery sequence

1. Finish and verify the foundations projects; extract reusable interfaces only after real duplication appears.
2. Build MCP server/client and multi-server tool discovery examples.
3. Build RAG ingestion, retrieval, citation, and evaluation foundations.
4. Build stateful orchestration with persistence, retries, idempotency, and human approval.
5. Build developer and DevOps agents with read-only defaults and explicit approval for mutations.
6. Expand domain, advanced interface, security, and research/productivity projects.
7. Revisit the catalogue regularly to merge duplicates, retire obsolete ideas, and update dependencies.

## Definition of done

A project is **Verified** only when clean setup, main scenario, automated tests, important failure paths, secrets handling, permissions, and safe logging are demonstrated. A project is **Production-oriented** only when deployment, health checks, observability, resource limits, scaling, threat model, and operational recovery are also documented.

Never count a planned catalogue entry as an implemented project.
