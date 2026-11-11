# AI Agents Projects

A hands-on engineering collection of AI agents: from first principles to reliable, observable, secure systems.

The repository now has a **500-project catalogue across 10 engineering tracks**. The catalogue is a coverage map, not a claim that 500 implementations already exist. Projects are built and verified incrementally; quality takes priority over folder count.

## Start here

- [Browse all 500 projects](docs/PROJECT_CATALOG.md)
- [Machine-readable JSON catalogue](catalogue/projects.json)
- [CSV catalogue](catalogue/projects.csv)
- [Implementation roadmap](docs/ROADMAP.md)
- [Project implementation standard](docs/PROJECT_STANDARD.md)

## Repository tracks

| Track | Purpose |
|---|---|
| [01 Foundations](01-foundations/) | LLM calls, structured output, tools, state, memory, and loops |
| [02 RAG agents](02-rag-agents/) | Retrieval, grounding, citations, and data assistants |
| [03 MCP agents](03-mcp-agents/) | MCP clients, servers, discovery, and integrations |
| [04 Orchestration](04-orchestration/) | Stateful workflows, planning, routing, and multi-agent systems |
| [05 Developer agents](05-developer-agents/) | Code review, debugging, testing, and repository automation |
| [06 DevOps agents](06-devops-agents/) | Logs, incidents, Kubernetes, cloud, and SRE workflows |
| [07 Domain agents](07-domain-agents/) | Business and industry-specific workflows |
| [08 Advanced agents](08-advanced-agents/) | Browser, voice, multimodal, and long-running workflows |
| [09 Security and evaluation](09-security-evaluation/) | Guardrails, threat testing, evaluation, and governance |
| [10 Research and productivity](10-research-productivity/) | Research, knowledge management, and productivity workflows |

## Implemented project foundations

| ID | Project | Status |
|---|---|---|
| AG-001 | [Tool-calling agent](01-foundations/01-tool-calling-agent/) | In progress — local verification pending |
| AG-002 | [Structured-output agent](01-foundations/02-structured-output-agent/) | In progress — local verification pending |
| AG-003 | [System and developer prompt boundary demo](01-foundations/03-system-and-developer-prompt-boundary-demo/) | In progress — local verification pending |
| AG-004 | [Conversation history manager](01-foundations/04-conversation-history-manager/) | In progress — local verification pending |
| AG-005 | [Token budget estimator](01-foundations/05-token-budget-estimator/) | In progress — local verification pending |
| AG-006 | [Context-window truncation strategy](01-foundations/06-context-window-truncation/) | In progress — local verification pending |
| AG-007 | [Evidence-backed entity extraction agent](01-foundations/07-evidence-backed-entity-extraction-agent/) | In progress — local verification pending |
| AG-008 | [Schema repair and retry agent](01-foundations/08-schema-repair-and-retry-agent/) | In progress — local verification pending |
| AG-009 | [Tool-calling calculator](01-foundations/09-tool-calling-calculator/) | In progress — local verification pending |
| AG-010 | [Multi-tool selection agent](01-foundations/10-multi-tool-selection-agent/) | In progress — local verification pending |

## Engineering principles

1. Runnable code beats screenshots and pseudo-code.
2. A model proposes; deterministic application code validates and executes.
3. Tools use explicit schemas, allowlists, timeouts, and auditable results.
4. State and memory are explicit, scoped, and inspectable.
5. Every project tests important behavior and failure paths.
6. Secrets are never committed; configuration is documented safely.
7. Human approval is required for consequential or irreversible actions.
8. Provider and framework choices are isolated behind adapters where useful.
9. Production-oriented claims require evidence: tests, security, observability, and operational docs.
10. Local models such as Ollama are supported where practical; cloud APIs remain optional when possible.

## Project maturity

- **Planned:** catalogued; no implementation claim.
- **In progress:** implementation is being built; verification may be pending.
- **Implemented:** main flow runs and basic tests pass.
- **Verified:** reproducible setup and important failure cases pass.
- **Production-oriented:** deployment, security, observability, limits, and operational guidance are included.

## Local development

Python 3.12+ is the default for new Python projects unless a framework has a documented compatibility constraint. Each project has its own environment and setup instructions.

```bash
git clone https://github.com/BharatJogi777/AI-Agents-Projects.git
cd AI-Agents-Projects
```

## Safety

Agents must not receive unrestricted shell, filesystem, database, browser, or cloud access. Use least-privilege tools, validation, allowlists, execution limits, approval gates, and audit logs. Treat retrieved documents and tool outputs as untrusted data.

## Reference material and attribution

The catalogue is informed by public agent projects and learning resources, including [500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects). This is an independent implementation effort, not a mirror. External code/assets are reused only when licences permit it and attribution requirements are met.

## Contributing

Follow [PROJECT_STANDARD.md](docs/PROJECT_STANDARD.md). Every implementation needs a clear use case, architecture, setup, runnable example, tests, limitations, and security notes.

## License

A repository licence will be selected before external contributions or third-party code reuse. Individual third-party components retain their original licences and notices.


## Newly implemented foundations (AG-021–AG-030)

- [x] AG-021 — OpenAI-compatible API adapter: OpenAI-compatible chat-completions HTTP adapter (local verification pending).
- [x] AG-022 — Model capability registry: Capability metadata, registration, filtering, and deterministic selection (local verification pending).
- [x] AG-023 — Model fallback router: Capability-aware provider routing and sequential fallback (local verification pending).
- [x] AG-024 — Streaming response agent: SSE frame parsing, incremental text events, and stream completion (local verification pending).
- [x] AG-025 — Incremental JSON stream parser: Incremental JSON decoding and buffer limits (local verification pending).
- [x] AG-026 — Function-call parser: Function-call parsing, allowlist validation, and dispatch boundary (local verification pending).
- [x] AG-027 — Model output parser benchmark: Parser correctness gates and throughput measurement (local verification pending).
- [x] AG-028 — Deterministic rule plus LLM router: Rule-first routing with constrained LLM fallback (local verification pending).
- [x] AG-029 — Intent classification agent: Typed intent output, confidence threshold, and review flag (local verification pending).
- [x] AG-030 — Entity extraction agent: Evidence-grounded entity extraction and validation (local verification pending).


## Newly implemented foundations (AG-041–AG-050)

- [x] AG-041 — Agent state machine: State transitions and terminal-state enforcement (local verification pending).
- [x] AG-042 — Agent run lifecycle manager: Run lifecycle, timestamps, isolation, and locking (local verification pending).
- [x] AG-043 — Idempotent tool execution: Idempotency keys, payload fingerprints, replay, and conflict detection (local verification pending).
- [x] AG-044 — Agent cancellation handler: Cooperative cancellation and reason propagation (local verification pending).
- [x] AG-045 — Run budget and step limiter: Step, deadline, and cost budget enforcement (local verification pending).
- [x] AG-046 — Prompt injection awareness demo: Trusted/untrusted boundaries and deterministic policy checks (local verification pending).
- [x] AG-047 — Untrusted tool-output handling: Bounded serialization, redaction, and untrusted labeling (local verification pending).
- [x] AG-048 — Agent trace event emitter: Structured events, ordering, bounds, and redaction (local verification pending).
- [x] AG-049 — CLI agent interface: CLI boundary, validation, dependency injection, and exit codes (local verification pending).
- [x] AG-050 — FastAPI agent endpoint: HTTP API boundary, typed validation, injection, and safe error mapping (local verification pending).

## RAG and data agents implemented (AG-051–AG-060)

- [x] AG-051 — PDF question-answering agent: Extract page-aware text from PDF files and return bounded evidence snippets with page numbers for downstream grounded answers. (local verification pending).
- [x] AG-052 — DOCX knowledge assistant: Extract DOCX paragraphs and table rows in document order, retaining structural labels so retrieved evidence can be traced to its source. (local verification pending).
- [x] AG-053 — Markdown documentation assistant: Split Markdown documentation into heading-aware chunks while retaining heading paths, source line ranges, and original text for citations. (local verification pending).
- [x] AG-054 — HTML knowledge-base agent: Extract readable HTML text while excluding script, style, and hidden content; retain headings and links as text for safer knowledge ingestion. (local verification pending).
- [x] AG-055 — CSV question-answering agent: Turn CSV rows into evidence-bearing records with row numbers, strict headers, bounded file size, and safe handling of quoted delimiters. (local verification pending).
- [x] AG-056 — Excel workbook analyst: Read Excel worksheets in read-only mode, preserve sheet and row provenance, and bound workbook size and row counts. (local verification pending).
- [x] AG-057 — JSON dataset assistant: Normalize JSON objects and arrays into bounded records with stable JSON paths and canonical serialization for evidence and indexing. (local verification pending).
- [x] AG-058 — Multi-format document ingester: Provide one bounded ingestion interface for TXT, Markdown, HTML, CSV, JSON, PDF, DOCX, and XLSX while retaining source-specific provenance. (local verification pending).
- [x] AG-059 — Directory watcher ingestion agent: Poll a document directory safely and emit deterministic created, modified, and deleted events using content hashes without following symlinks. (local verification pending).
- [x] AG-060 — Incremental document indexer: Maintain a transactional SQLite document and chunk index using content hashes, deterministic chunk IDs, and unchanged-document skips. (local verification pending).

## Retrieval agents implemented (AG-061–AG-070)

- [x] AG-061 — Document deduplication agent: Detect exact duplicates using SHA-256 and normalized text; report groups without automatically deleting source records. (local verification pending).
- [x] AG-062 — Document metadata extractor: Extract deterministic file metadata including name, media type, byte size, modification time, and content digest. (local verification pending).
- [x] AG-063 — Semantic chunking pipeline: Split text at injected semantic similarity boundaries while retaining source offsets. (local verification pending).
- [x] AG-064 — Parent-child chunk retrieval: Store larger parent passages and smaller searchable child chunks, then expand matched children to parent context. (local verification pending).
- [x] AG-065 — Sliding-window chunker: Generate overlapping text windows with stable offsets and validated size and overlap. (local verification pending).
- [x] AG-066 — Hybrid keyword-vector search agent: Combine lexical and vector rankings using reciprocal rank fusion. (local verification pending).
- [x] AG-067 — Metadata-filtered retrieval agent: Apply validated allowlisted metadata filters without evaluating user-supplied expressions. (local verification pending).
- [x] AG-068 — Query rewriting agent: Expand ambiguous queries using an injected rewriter while retaining the original and bounding variants. (local verification pending).
- [x] AG-069 — Multi-query retrieval agent: Retrieve across query variants, deduplicate candidates, and fuse ranks using reciprocal rank fusion. (local verification pending).
- [x] AG-070 — HyDE retrieval agent: Generate a hypothetical document for query expansion while never treating generated text as evidence. (local verification pending).

## Grounded answering and graph retrieval (AG-071–AG-080)

- [x] AG-071 — Cross-encoder reranking agent: Rerank retrieved passages using an injected query-passage relevance scorer with deterministic ordering. (local verification pending).
- [x] AG-072 — Context compression agent: Compress retrieved context by selecting exact relevant spans while preserving source offsets. (local verification pending).
- [x] AG-073 — Citation-grounded answer agent: Construct claim-level answers whose citations must resolve to supplied source records. (local verification pending).
- [x] AG-074 — Citation verification agent: Verify citation source IDs and exact quoted substrings against the original source text. (local verification pending).
- [x] AG-075 — Evidence coverage evaluator: Measure claim-level evidence coverage and flag uncited or unknown-source claims. (local verification pending).
- [x] AG-076 — Abstention-on-no-evidence agent: Abstain when retrieved evidence is absent or fails a configured score and source-count policy. (local verification pending).
- [x] AG-077 — Multi-hop retrieval agent: Run bounded sequential retrieval hops, preserving provenance and deduplicating evidence. (local verification pending).
- [x] AG-078 — Knowledge graph RAG agent: Validate source-backed entity-relation triples and retrieve facts connected to a requested entity. (local verification pending).
- [x] AG-079 — Graph traversal question-answering agent: Find bounded graph paths with cycle prevention and evidence IDs on every edge. (local verification pending).
- [x] AG-080 — SQL database question-answering agent: Execute bounded read-only SQLite SELECT queries with table allowlists and an authorizer. (local verification pending).
