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
- [x] AG-010 Multi-tool selection agent: model selection across three typed, allowlisted tools with bounded execution (local verification pending).
- [x] AG-011 Typed tool registry: provider schema export, duplicate registration checks, Pydantic validation, and controlled handler failures (local verification pending).
- [x] AG-012 Tool argument validation gate: allowlist checks, JSON parsing, strict Pydantic validation, and separate handler failure handling (local verification pending).
- [x] AG-013 Tool result normalization: bounded JSON-safe output, secret redaction, cycle handling, and truncation warnings (local verification pending).
- [x] AG-014 Bounded agent loop: independent step, tool-call, and consecutive-error limits (local verification pending).
- [x] AG-015 Stop-condition and loop detector: stable state fingerprints, bounded repeat history, and deterministic stop priority (local verification pending).
- [x] AG-016 Tool timeout handler: async deadlines, cancellation propagation, and typed timeout errors (local verification pending).
- [x] AG-017 Retry with exponential backoff: bounded attempts, exponential delays, jitter, and retry classification (local verification pending).
- [x] AG-018 Circuit-breaker model client: thread-safe state transitions, recovery window, and a single half-open probe (local verification pending).
- [x] AG-019 Provider-agnostic LLM adapter: normalized chat contracts and provider routing (local verification pending).
- [x] AG-020 Ollama local model adapter: non-streaming chat, health/model listing, and provider error normalization (local verification pending).
- [x] AG-021 OpenAI-compatible API adapter: Implement a normalized non-streaming chat adapter for OpenAI-compatible endpoints, including request mapping, bearer authentication, response validation, and usage normalization. (local verification pending).
- [x] AG-022 Model capability registry: Register explicit provider/model capability metadata and select models by required features and context capacity. (local verification pending).
- [x] AG-023 Model fallback router: Route generation requests across compatible providers and models using health checks, provider preferences, and sequential fallback. (local verification pending).
- [x] AG-024 Streaming response agent: Parse fragmented Server-Sent Event frames into incremental assistant text and terminal completion events. (local verification pending).
- [x] AG-025 Incremental JSON stream parser: Decode JSON values arriving across arbitrary text chunks with bounded buffering and end-of-stream validation. (local verification pending).
- [x] AG-026 Function-call parser: Normalize provider function-call payloads, validate call identifiers and allowlisted names, and reject malformed or oversized arguments. (local verification pending).
- [x] AG-027 Model output parser benchmark: Benchmark parser implementations only after correctness checks, reporting throughput and elapsed time for repeatable input cases. (local verification pending).
- [x] AG-028 Deterministic rule plus LLM router: Apply deterministic routing rules first and invoke an LLM classifier only for unmatched inputs, constraining output to an allowlist. (local verification pending).
- [x] AG-029 Intent classification agent: Validate classifier output against an intent allowlist and confidence threshold, escalating low-confidence results for human review. (local verification pending).
- [x] AG-030 Entity extraction agent: Validate extracted entities against source evidence, allowed types, source offsets, input limits, and duplicate handling. (local verification pending).
- [ ] Run AG-001 and AG-002 in clean Python 3.12 environments and verify Ollama integration; run AG-003 tests and CLI locally; run AG-004 tests and history demo; run AG-005 tests and budget demo; run AG-006 tests and truncation demo; run AG-007 tests and entity extraction demo; run AG-008 tests and repair/retry demo; run AG-009 calculator tests and Ollama tool-call demo; run AG-010 multi-tool selection tests and model demo; run AG-011 registry tests; run AG-012 validation gate tests; run AG-013 normalization tests; run AG-014 loop-budget tests; run AG-015 detector tests; run AG-016 async timeout tests; run AG-017 retry tests; run AG-018 circuit-breaker tests; run AG-019 provider-contract tests; run AG-020 Ollama adapter tests and local integration; run AG-021 to AG-030 tests in their project directories.

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


## Newly implemented foundations (AG-031–AG-040)

- [x] AG-031 Task decomposition agent: Decompose an objective into atomic tasks with stable IDs and dependencies; reject malformed or cyclic graphs. (local verification pending).
- [x] AG-032 Plan generation agent: Generate a typed execution plan through an injected planner, enforcing task limits and a stable JSON contract. (local verification pending).
- [x] AG-033 Plan validation agent: Validate plans for unique IDs, valid dependencies, acyclic ordering, bounded actions, and allowed risk before execution. (local verification pending).
- [x] AG-034 Plan execution tracker: Track step state transitions and dependency readiness with idempotent completion and explicit failure recovery. (local verification pending).
- [x] AG-035 Short-term conversation memory: Maintain a bounded chronological message window while preserving system instructions and complete turns. (local verification pending).
- [x] AG-036 Session-scoped memory store: Provide thread-safe session-isolated key/value memory with TTL, injectable clock, and bounded capacity. (local verification pending).
- [x] AG-037 User preference memory prototype: Store only explicit, user-confirmed non-sensitive preferences with provenance and user-controlled deletion. (local verification pending).
- [x] AG-038 Memory summarization agent: Compress conversation through an injected summarizer while enforcing source and summary limits. (local verification pending).
- [x] AG-039 Memory retrieval policy demo: Rank memory candidates using query overlap, recency, and confidence while filtering expired and unconfirmed records. (local verification pending).
- [x] AG-040 Human approval checkpoint: Pause consequential actions behind expiring one-time approval requests bound to an immutable action payload hash. (local verification pending).
