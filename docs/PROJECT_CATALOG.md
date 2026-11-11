# Project Catalogue — 500 AI Agent Projects

This is the master index for the repository. It contains **500 distinct project specifications** across 10 tracks. A catalogue entry is a scope definition, not a claim that its code exists or is production-ready.

## Track overview

| Track | Projects | Focus |
|---|---:|---|
| [Foundations](../01-foundations/README.md) | 50 | Core agent loop, typed I/O, tools, state, and control flow |
| [RAG and Data Agents](../02-rag-agents/README.md) | 50 | Ingestion, retrieval, grounding, data access, and evaluation |
| [MCP and Tool Integration](../03-mcp-agents/README.md) | 50 | MCP servers, clients, discovery, transport, permissions, and resilience |
| [Orchestration and Multi-Agent Systems](../04-orchestration/README.md) | 50 | Stateful graphs, routing, delegation, planning, and human control |
| [Developer and Software Engineering Agents](../05-developer-agents/README.md) | 50 | Repository understanding, coding support, testing, review, and delivery |
| [DevOps, SRE, and Cloud Operations Agents](../06-devops-agents/README.md) | 50 | Read-only diagnostics first, bounded remediation, incident workflows |
| [Business and Industry Domain Agents](../07-domain-agents/README.md) | 50 | Human-supervised domain workflows with explicit evidence and permissions |
| [Advanced Interfaces and Autonomous Workflows](../08-advanced-agents/README.md) | 50 | Browser, voice, multimodal, event-driven, and long-running agents |
| [Security, Governance, and Evaluation](../09-security-evaluation/README.md) | 50 | Threat modeling, policy enforcement, testing, evaluation, and auditability |
| [Research, Knowledge, and Productivity Agents](../10-research-productivity/README.md) | 50 | Evidence gathering, synthesis, knowledge workflows, and personal productivity |

## Status policy

- **In progress:** implementation exists but local verification is pending.
- **Planned:** catalogued, not yet implemented.
- **Implemented / Verified / Production-oriented:** only assigned when the evidence requirements in [PROJECT_STANDARD.md](PROJECT_STANDARD.md) are met.

Current implementation status: AG-001 through AG-016 are in progress. The other 484 entries are planned.

## How to use this catalogue

1. Search by ID, title, track, or tag in [projects.json](../catalogue/projects.json) or [projects.csv](../catalogue/projects.csv).
2. Read the track README for the engineering expectations.
3. Before implementing a project, check whether an existing project already covers the same capability.
4. Create the project using [PROJECT_STANDARD.md](PROJECT_STANDARD.md).
5. Update the machine-readable status only after the corresponding evidence exists.

## Project index

### Foundations

| ID | Project | Difficulty | Status |
|---|---|---|---|
| AG-001 | Bounded tool-calling agent | Beginner to intermediate | In progress |
| AG-002 | Schema-constrained structured-output agent | Beginner to intermediate | In progress |
| AG-003 | System and developer prompt boundary demo | Beginner to intermediate | In progress |
| AG-004 | Conversation history manager | Beginner to intermediate | In progress |
| AG-005 | Token budget estimator | Beginner to intermediate | In progress |
| AG-006 | Context-window truncation strategy | Beginner to intermediate | In progress |
| AG-007 | Evidence-backed entity extraction agent | Beginner to intermediate | In progress |
| AG-008 | Schema repair and retry agent | Beginner to intermediate | In progress |
| AG-009 | Tool-calling calculator | Beginner to intermediate | In progress |
| AG-010 | Multi-tool selection agent | Beginner to intermediate | In progress |
| AG-011 | Typed tool registry | Beginner to intermediate | In progress |
| AG-012 | Tool argument validation agent | Beginner to intermediate | In progress |
| AG-013 | Tool result normalization agent | Beginner to intermediate | In progress |
| AG-014 | Bounded agent loop | Beginner to intermediate | In progress |
| AG-015 | Stop-condition and loop detector | Beginner to intermediate | In progress |
| AG-016 | Tool timeout handler | Beginner to intermediate | In progress |
| AG-017 | Retry with exponential backoff | Beginner to intermediate | Planned |
| AG-018 | Circuit-breaker model client | Beginner to intermediate | Planned |
| AG-019 | Provider-agnostic LLM adapter | Beginner to intermediate | Planned |
| AG-020 | Ollama local model adapter | Beginner to intermediate | Planned |
| AG-021 | OpenAI-compatible API adapter | Beginner to intermediate | Planned |
| AG-022 | Model capability registry | Beginner to intermediate | Planned |
| AG-023 | Model fallback router | Beginner to intermediate | Planned |
| AG-024 | Streaming response agent | Beginner to intermediate | Planned |
| AG-025 | Incremental JSON stream parser | Beginner to intermediate | Planned |
| AG-026 | Function-call parser | Beginner to intermediate | Planned |
| AG-027 | Model output parser benchmark | Beginner to intermediate | Planned |
| AG-028 | Deterministic rule plus LLM router | Beginner to intermediate | Planned |
| AG-029 | Intent classification agent | Beginner to intermediate | Planned |
| AG-030 | Entity extraction agent | Beginner to intermediate | Planned |
| AG-031 | Task decomposition agent | Beginner to intermediate | Planned |
| AG-032 | Plan generation agent | Beginner to intermediate | Planned |
| AG-033 | Plan validation agent | Beginner to intermediate | Planned |
| AG-034 | Plan execution tracker | Beginner to intermediate | Planned |
| AG-035 | Short-term conversation memory | Beginner to intermediate | Planned |
| AG-036 | Session-scoped memory store | Beginner to intermediate | Planned |
| AG-037 | User preference memory prototype | Beginner to intermediate | Planned |
| AG-038 | Memory summarization agent | Beginner to intermediate | Planned |
| AG-039 | Memory retrieval policy demo | Beginner to intermediate | Planned |
| AG-040 | Human approval checkpoint | Beginner to intermediate | Planned |
| AG-041 | Agent state machine | Beginner to intermediate | Planned |
| AG-042 | Agent run lifecycle manager | Beginner to intermediate | Planned |
| AG-043 | Idempotent tool execution | Beginner to intermediate | Planned |
| AG-044 | Agent cancellation handler | Beginner to intermediate | Planned |
| AG-045 | Run budget and step limiter | Beginner to intermediate | Planned |
| AG-046 | Prompt injection awareness demo | Beginner to intermediate | Planned |
| AG-047 | Untrusted tool-output handling | Beginner to intermediate | Planned |
| AG-048 | Agent trace event emitter | Beginner to intermediate | Planned |
| AG-049 | CLI agent interface | Beginner to intermediate | Planned |
| AG-050 | FastAPI agent endpoint | Beginner to intermediate | Planned |

### RAG and Data Agents

| ID | Project | Difficulty | Status |
|---|---|---|---|
| AG-051 | PDF question-answering agent | Intermediate | Planned |
| AG-052 | DOCX knowledge assistant | Intermediate | Planned |
| AG-053 | Markdown documentation assistant | Intermediate | Planned |
| AG-054 | HTML knowledge-base agent | Intermediate | Planned |
| AG-055 | CSV question-answering agent | Intermediate | Planned |
| AG-056 | Excel workbook analyst | Intermediate | Planned |
| AG-057 | JSON dataset assistant | Intermediate | Planned |
| AG-058 | Multi-format document ingester | Intermediate | Planned |
| AG-059 | Directory watcher ingestion agent | Intermediate | Planned |
| AG-060 | Incremental document indexer | Intermediate | Planned |
| AG-061 | Document deduplication agent | Intermediate | Planned |
| AG-062 | Document metadata extractor | Intermediate | Planned |
| AG-063 | Semantic chunking pipeline | Intermediate | Planned |
| AG-064 | Parent-child chunk retrieval | Intermediate | Planned |
| AG-065 | Sliding-window chunker | Intermediate | Planned |
| AG-066 | Hybrid keyword-vector search agent | Intermediate | Planned |
| AG-067 | Metadata-filtered retrieval agent | Intermediate | Planned |
| AG-068 | Query rewriting agent | Intermediate | Planned |
| AG-069 | Multi-query retrieval agent | Intermediate | Planned |
| AG-070 | HyDE retrieval agent | Intermediate | Planned |
| AG-071 | Cross-encoder reranking agent | Intermediate | Planned |
| AG-072 | Context compression agent | Intermediate | Planned |
| AG-073 | Citation-grounded answer agent | Intermediate | Planned |
| AG-074 | Citation verification agent | Intermediate | Planned |
| AG-075 | Evidence coverage evaluator | Intermediate | Planned |
| AG-076 | Abstention-on-no-evidence agent | Intermediate | Planned |
| AG-077 | Multi-hop retrieval agent | Intermediate | Planned |
| AG-078 | Knowledge graph RAG agent | Intermediate | Planned |
| AG-079 | Graph traversal question-answering agent | Intermediate | Planned |
| AG-080 | SQL database question-answering agent | Intermediate | Planned |
| AG-081 | Read-only text-to-SQL agent | Intermediate | Planned |
| AG-082 | SQL query validator | Intermediate | Planned |
| AG-083 | SQL result explanation agent | Intermediate | Planned |
| AG-084 | Natural-language analytics agent | Intermediate | Planned |
| AG-085 | Time-series data analyst | Intermediate | Planned |
| AG-086 | Pandas data assistant | Intermediate | Planned |
| AG-087 | Data profiling agent | Intermediate | Planned |
| AG-088 | Data quality issue detector | Intermediate | Planned |
| AG-089 | Schema discovery agent | Intermediate | Planned |
| AG-090 | Database documentation assistant | Intermediate | Planned |
| AG-091 | API documentation RAG agent | Intermediate | Planned |
| AG-092 | Codebase retrieval assistant | Intermediate | Planned |
| AG-093 | Repository architecture Q&A agent | Intermediate | Planned |
| AG-094 | Multilingual document retrieval | Intermediate | Planned |
| AG-095 | Image-caption retrieval assistant | Intermediate | Planned |
| AG-096 | Audio transcript retrieval agent | Intermediate | Planned |
| AG-097 | RAG freshness monitor | Intermediate | Planned |
| AG-098 | Retrieval regression evaluator | Intermediate | Planned |
| AG-099 | RAG answer benchmark runner | Intermediate | Planned |
| AG-100 | RAG access-control filter | Intermediate | Planned |

### MCP and Tool Integration

| ID | Project | Difficulty | Status |
|---|---|---|---|
| AG-101 | First MCP server with typed tools | Intermediate to advanced | Planned |
| AG-102 | MCP server resource browser | Intermediate to advanced | Planned |
| AG-103 | MCP prompt-template server | Intermediate to advanced | Planned |
| AG-104 | MCP client tool discovery | Intermediate to advanced | Planned |
| AG-105 | MCP client tool invocation | Intermediate to advanced | Planned |
| AG-106 | MCP stdio transport client | Intermediate to advanced | Planned |
| AG-107 | MCP HTTP transport client | Intermediate to advanced | Planned |
| AG-108 | MCP server health inspector | Intermediate to advanced | Planned |
| AG-109 | MCP tool schema validator | Intermediate to advanced | Planned |
| AG-110 | MCP tool namespace manager | Intermediate to advanced | Planned |
| AG-111 | Multi-server MCP client | Intermediate to advanced | Planned |
| AG-112 | MCP server connection pool | Intermediate to advanced | Planned |
| AG-113 | MCP reconnecting client | Intermediate to advanced | Planned |
| AG-114 | MCP request timeout manager | Intermediate to advanced | Planned |
| AG-115 | MCP cancellation propagation | Intermediate to advanced | Planned |
| AG-116 | MCP authorization gateway | Intermediate to advanced | Planned |
| AG-117 | Per-tool permission policy | Intermediate to advanced | Planned |
| AG-118 | MCP audit logging server | Intermediate to advanced | Planned |
| AG-119 | MCP rate-limited tool server | Intermediate to advanced | Planned |
| AG-120 | MCP pagination tool server | Intermediate to advanced | Planned |
| AG-121 | MCP file metadata server | Intermediate to advanced | Planned |
| AG-122 | Read-only filesystem MCP server | Intermediate to advanced | Planned |
| AG-123 | Safe document search MCP server | Intermediate to advanced | Planned |
| AG-124 | PostgreSQL read-only MCP server | Intermediate to advanced | Planned |
| AG-125 | Redis diagnostics MCP server | Intermediate to advanced | Planned |
| AG-126 | Git repository MCP server | Intermediate to advanced | Planned |
| AG-127 | GitHub issue MCP integration | Intermediate to advanced | Planned |
| AG-128 | GitHub pull-request MCP assistant | Intermediate to advanced | Planned |
| AG-129 | Jira MCP integration | Intermediate to advanced | Planned |
| AG-130 | Slack MCP integration | Intermediate to advanced | Planned |
| AG-131 | Email drafting MCP server | Intermediate to advanced | Planned |
| AG-132 | Calendar availability MCP server | Intermediate to advanced | Planned |
| AG-133 | Cloud inventory MCP server | Intermediate to advanced | Planned |
| AG-134 | Kubernetes read-only MCP server | Intermediate to advanced | Planned |
| AG-135 | Docker inspection MCP server | Intermediate to advanced | Planned |
| AG-136 | Observability query MCP server | Intermediate to advanced | Planned |
| AG-137 | Prometheus MCP integration | Intermediate to advanced | Planned |
| AG-138 | Grafana dashboard MCP tool | Intermediate to advanced | Planned |
| AG-139 | Browser search MCP server | Intermediate to advanced | Planned |
| AG-140 | Internal REST API MCP adapter | Intermediate to advanced | Planned |
| AG-141 | OpenAPI-to-MCP tool generator | Intermediate to advanced | Planned |
| AG-142 | MCP tool contract test harness | Intermediate to advanced | Planned |
| AG-143 | MCP server conformance tester | Intermediate to advanced | Planned |
| AG-144 | MCP prompt-injection boundary demo | Intermediate to advanced | Planned |
| AG-145 | MCP secret redaction middleware | Intermediate to advanced | Planned |
| AG-146 | MCP multi-tenant isolation demo | Intermediate to advanced | Planned |
| AG-147 | MCP server deployment template | Intermediate to advanced | Planned |
| AG-148 | MCP tool latency monitor | Intermediate to advanced | Planned |
| AG-149 | MCP server policy simulator | Intermediate to advanced | Planned |
| AG-150 | MCP tool registry catalog | Intermediate to advanced | Planned |

### Orchestration and Multi-Agent Systems

| ID | Project | Difficulty | Status |
|---|---|---|---|
| AG-151 | Sequential workflow agent | Intermediate to advanced | Planned |
| AG-152 | Conditional workflow router | Intermediate to advanced | Planned |
| AG-153 | Parallel task executor | Intermediate to advanced | Planned |
| AG-154 | Fan-out fan-in research workflow | Intermediate to advanced | Planned |
| AG-155 | Planner-executor graph | Intermediate to advanced | Planned |
| AG-156 | Plan-and-replan workflow | Intermediate to advanced | Planned |
| AG-157 | Supervisor-worker team | Intermediate to advanced | Planned |
| AG-158 | Hierarchical agent team | Intermediate to advanced | Planned |
| AG-159 | Researcher-writer-editor team | Intermediate to advanced | Planned |
| AG-160 | Debate and consensus workflow | Intermediate to advanced | Planned |
| AG-161 | Critic-revision workflow | Intermediate to advanced | Planned |
| AG-162 | Self-reflection loop with limits | Intermediate to advanced | Planned |
| AG-163 | Tool router graph | Intermediate to advanced | Planned |
| AG-164 | Intent-based specialist router | Intermediate to advanced | Planned |
| AG-165 | Mixture-of-experts agent router | Intermediate to advanced | Planned |
| AG-166 | Human-in-the-loop approval graph | Intermediate to advanced | Planned |
| AG-167 | Escalation and handoff workflow | Intermediate to advanced | Planned |
| AG-168 | Checkpointed workflow agent | Intermediate to advanced | Planned |
| AG-169 | Persistent workflow state store | Intermediate to advanced | Planned |
| AG-170 | Workflow resume after restart | Intermediate to advanced | Planned |
| AG-171 | Long-running task coordinator | Intermediate to advanced | Planned |
| AG-172 | Durable job queue agent | Intermediate to advanced | Planned |
| AG-173 | Compensating action workflow | Intermediate to advanced | Planned |
| AG-174 | Saga-style agent workflow | Intermediate to advanced | Planned |
| AG-175 | Idempotent workflow step runner | Intermediate to advanced | Planned |
| AG-176 | Distributed task delegation | Intermediate to advanced | Planned |
| AG-177 | Agent message envelope protocol | Intermediate to advanced | Planned |
| AG-178 | Multi-agent shared blackboard | Intermediate to advanced | Planned |
| AG-179 | Role-based agent collaboration | Intermediate to advanced | Planned |
| AG-180 | Dynamic team composition agent | Intermediate to advanced | Planned |
| AG-181 | Agent task auction prototype | Intermediate to advanced | Planned |
| AG-182 | Agent negotiation simulator | Intermediate to advanced | Planned |
| AG-183 | Conflict resolution coordinator | Intermediate to advanced | Planned |
| AG-184 | Multi-agent memory isolation | Intermediate to advanced | Planned |
| AG-185 | Shared knowledge workspace | Intermediate to advanced | Planned |
| AG-186 | Agent result aggregator | Intermediate to advanced | Planned |
| AG-187 | Subtask dependency scheduler | Intermediate to advanced | Planned |
| AG-188 | Workflow deadline manager | Intermediate to advanced | Planned |
| AG-189 | Workflow cancellation coordinator | Intermediate to advanced | Planned |
| AG-190 | Workflow event streaming API | Intermediate to advanced | Planned |
| AG-191 | Graph visualization exporter | Intermediate to advanced | Planned |
| AG-192 | Workflow replay debugger | Intermediate to advanced | Planned |
| AG-193 | Deterministic workflow test harness | Intermediate to advanced | Planned |
| AG-194 | Agent handoff contract validator | Intermediate to advanced | Planned |
| AG-195 | Multi-agent cost budget manager | Intermediate to advanced | Planned |
| AG-196 | Multi-agent observability trace | Intermediate to advanced | Planned |
| AG-197 | Agent workflow version migration | Intermediate to advanced | Planned |
| AG-198 | Approval-aware tool orchestration | Intermediate to advanced | Planned |
| AG-199 | Parallel retrieval and synthesis | Intermediate to advanced | Planned |
| AG-200 | Fallback workflow orchestration | Intermediate to advanced | Planned |

### Developer and Software Engineering Agents

| ID | Project | Difficulty | Status |
|---|---|---|---|
| AG-201 | Repository onboarding assistant | Intermediate to advanced | Planned |
| AG-202 | Codebase architecture explainer | Intermediate to advanced | Planned |
| AG-203 | Symbol and dependency explorer | Intermediate to advanced | Planned |
| AG-204 | Code search assistant | Intermediate to advanced | Planned |
| AG-205 | Pull request summarizer | Intermediate to advanced | Planned |
| AG-206 | Pull request review assistant | Intermediate to advanced | Planned |
| AG-207 | Bug reproduction planner | Intermediate to advanced | Planned |
| AG-208 | Issue triage classifier | Intermediate to advanced | Planned |
| AG-209 | Issue-to-plan agent | Intermediate to advanced | Planned |
| AG-210 | Feature implementation planner | Intermediate to advanced | Planned |
| AG-211 | Code change proposal agent | Intermediate to advanced | Planned |
| AG-212 | Patch generation assistant | Intermediate to advanced | Planned |
| AG-213 | Patch validation agent | Intermediate to advanced | Planned |
| AG-214 | Unit test generator | Intermediate to advanced | Planned |
| AG-215 | Integration test planner | Intermediate to advanced | Planned |
| AG-216 | Property-based test generator | Intermediate to advanced | Planned |
| AG-217 | Regression test selector | Intermediate to advanced | Planned |
| AG-218 | Flaky test investigator | Intermediate to advanced | Planned |
| AG-219 | Test failure diagnosis agent | Intermediate to advanced | Planned |
| AG-220 | Coverage gap analyst | Intermediate to advanced | Planned |
| AG-221 | Static analysis explanation agent | Intermediate to advanced | Planned |
| AG-222 | Linter remediation assistant | Intermediate to advanced | Planned |
| AG-223 | Type error diagnosis agent | Intermediate to advanced | Planned |
| AG-224 | Dependency upgrade planner | Intermediate to advanced | Planned |
| AG-225 | Dependency vulnerability explainer | Intermediate to advanced | Planned |
| AG-226 | License compliance assistant | Intermediate to advanced | Planned |
| AG-227 | API contract drift detector | Intermediate to advanced | Planned |
| AG-228 | OpenAPI spec reviewer | Intermediate to advanced | Planned |
| AG-229 | Database migration reviewer | Intermediate to advanced | Planned |
| AG-230 | SQL query review assistant | Intermediate to advanced | Planned |
| AG-231 | Performance hotspot investigator | Intermediate to advanced | Planned |
| AG-232 | Go code review assistant | Intermediate to advanced | Planned |
| AG-233 | Python code review assistant | Intermediate to advanced | Planned |
| AG-234 | TypeScript code review assistant | Intermediate to advanced | Planned |
| AG-235 | Concurrency bug investigator | Intermediate to advanced | Planned |
| AG-236 | Deadlock explanation agent | Intermediate to advanced | Planned |
| AG-237 | Memory leak investigation assistant | Intermediate to advanced | Planned |
| AG-238 | Refactoring planner | Intermediate to advanced | Planned |
| AG-239 | Design pattern advisor | Intermediate to advanced | Planned |
| AG-240 | Documentation generator | Intermediate to advanced | Planned |
| AG-241 | Changelog generator | Intermediate to advanced | Planned |
| AG-242 | Release note assistant | Intermediate to advanced | Planned |
| AG-243 | Commit message assistant | Intermediate to advanced | Planned |
| AG-244 | Git conflict resolution guide | Intermediate to advanced | Planned |
| AG-245 | Build failure investigator | Intermediate to advanced | Planned |
| AG-246 | CI log diagnosis assistant | Intermediate to advanced | Planned |
| AG-247 | Monorepo impact analyzer | Intermediate to advanced | Planned |
| AG-248 | Code ownership routing agent | Intermediate to advanced | Planned |
| AG-249 | Developer knowledge-base assistant | Intermediate to advanced | Planned |
| AG-250 | Secure coding review assistant | Intermediate to advanced | Planned |

### DevOps, SRE, and Cloud Operations Agents

| ID | Project | Difficulty | Status |
|---|---|---|---|
| AG-251 | Application log investigation agent | Advanced | Planned |
| AG-252 | Structured log anomaly explainer | Advanced | Planned |
| AG-253 | Trace investigation assistant | Advanced | Planned |
| AG-254 | Metrics query assistant | Advanced | Planned |
| AG-255 | Incident timeline builder | Advanced | Planned |
| AG-256 | Incident severity classifier | Advanced | Planned |
| AG-257 | On-call handoff summarizer | Advanced | Planned |
| AG-258 | Runbook retrieval assistant | Advanced | Planned |
| AG-259 | Runbook recommendation agent | Advanced | Planned |
| AG-260 | Kubernetes pod diagnosis agent | Advanced | Planned |
| AG-261 | Kubernetes event explainer | Advanced | Planned |
| AG-262 | Kubernetes deployment reviewer | Advanced | Planned |
| AG-263 | Kubernetes resource advisor | Advanced | Planned |
| AG-264 | Kubernetes capacity planner | Advanced | Planned |
| AG-265 | Kubernetes manifest security reviewer | Advanced | Planned |
| AG-266 | Docker image inspection agent | Advanced | Planned |
| AG-267 | Container startup failure investigator | Advanced | Planned |
| AG-268 | Helm values reviewer | Advanced | Planned |
| AG-269 | Terraform plan reviewer | Advanced | Planned |
| AG-270 | Terraform drift explainer | Advanced | Planned |
| AG-271 | AWS inventory assistant | Advanced | Planned |
| AG-272 | AWS cost anomaly investigator | Advanced | Planned |
| AG-273 | Cloud IAM policy reviewer | Advanced | Planned |
| AG-274 | Cloud security posture assistant | Advanced | Planned |
| AG-275 | VPC connectivity diagnosis agent | Advanced | Planned |
| AG-276 | Load balancer health investigator | Advanced | Planned |
| AG-277 | DNS failure investigator | Advanced | Planned |
| AG-278 | TLS certificate expiry monitor | Advanced | Planned |
| AG-279 | Database connection issue investigator | Advanced | Planned |
| AG-280 | PostgreSQL performance assistant | Advanced | Planned |
| AG-281 | Redis latency investigator | Advanced | Planned |
| AG-282 | Kafka consumer lag investigator | Advanced | Planned |
| AG-283 | Kafka topic configuration reviewer | Advanced | Planned |
| AG-284 | Queue backlog diagnosis agent | Advanced | Planned |
| AG-285 | Service dependency map builder | Advanced | Planned |
| AG-286 | SLO burn-rate explainer | Advanced | Planned |
| AG-287 | Error budget status assistant | Advanced | Planned |
| AG-288 | Capacity forecasting assistant | Advanced | Planned |
| AG-289 | Autoscaling recommendation agent | Advanced | Planned |
| AG-290 | Deployment risk assessor | Advanced | Planned |
| AG-291 | Canary analysis assistant | Advanced | Planned |
| AG-292 | Rollback recommendation agent | Advanced | Planned |
| AG-293 | Change impact analyzer | Advanced | Planned |
| AG-294 | Backup verification assistant | Advanced | Planned |
| AG-295 | Disaster recovery drill planner | Advanced | Planned |
| AG-296 | Secrets rotation planner | Advanced | Planned |
| AG-297 | Patch compliance assistant | Advanced | Planned |
| AG-298 | Cloud cost optimization planner | Advanced | Planned |
| AG-299 | Production readiness reviewer | Advanced | Planned |
| AG-300 | Incident postmortem drafter | Advanced | Planned |

### Business and Industry Domain Agents

| ID | Project | Difficulty | Status |
|---|---|---|---|
| AG-301 | Customer support triage agent | Intermediate to advanced | Planned |
| AG-302 | Customer support response drafter | Intermediate to advanced | Planned |
| AG-303 | Order status assistant | Intermediate to advanced | Planned |
| AG-304 | Refund eligibility checker | Intermediate to advanced | Planned |
| AG-305 | Returns workflow assistant | Intermediate to advanced | Planned |
| AG-306 | Subscription cancellation assistant | Intermediate to advanced | Planned |
| AG-307 | Sales lead qualification agent | Intermediate to advanced | Planned |
| AG-308 | Sales call preparation assistant | Intermediate to advanced | Planned |
| AG-309 | CRM data enrichment agent | Intermediate to advanced | Planned |
| AG-310 | Account health summarizer | Intermediate to advanced | Planned |
| AG-311 | Customer feedback theme analyzer | Intermediate to advanced | Planned |
| AG-312 | Voice-of-customer insight agent | Intermediate to advanced | Planned |
| AG-313 | Invoice extraction assistant | Intermediate to advanced | Planned |
| AG-314 | Invoice matching exception agent | Intermediate to advanced | Planned |
| AG-315 | Accounts payable review assistant | Intermediate to advanced | Planned |
| AG-316 | Expense policy checker | Intermediate to advanced | Planned |
| AG-317 | Purchase order assistant | Intermediate to advanced | Planned |
| AG-318 | Procurement comparison agent | Intermediate to advanced | Planned |
| AG-319 | Contract clause finder | Intermediate to advanced | Planned |
| AG-320 | Contract obligation tracker | Intermediate to advanced | Planned |
| AG-321 | Legal intake triage assistant | Intermediate to advanced | Planned |
| AG-322 | Compliance evidence collector | Intermediate to advanced | Planned |
| AG-323 | HR policy Q&A assistant | Intermediate to advanced | Planned |
| AG-324 | Resume screening workflow assistant | Intermediate to advanced | Planned |
| AG-325 | Interview question planner | Intermediate to advanced | Planned |
| AG-326 | Employee onboarding assistant | Intermediate to advanced | Planned |
| AG-327 | Training plan recommender | Intermediate to advanced | Planned |
| AG-328 | Meeting preparation assistant | Intermediate to advanced | Planned |
| AG-329 | Meeting action-item tracker | Intermediate to advanced | Planned |
| AG-330 | Calendar scheduling assistant | Intermediate to advanced | Planned |
| AG-331 | Travel itinerary planner | Intermediate to advanced | Planned |
| AG-332 | Travel expense audit assistant | Intermediate to advanced | Planned |
| AG-333 | Retail product discovery assistant | Intermediate to advanced | Planned |
| AG-334 | Retail inventory exception agent | Intermediate to advanced | Planned |
| AG-335 | Demand planning assistant | Intermediate to advanced | Planned |
| AG-336 | Supply-chain disruption monitor | Intermediate to advanced | Planned |
| AG-337 | Shipment exception investigator | Intermediate to advanced | Planned |
| AG-338 | Delivery route planning assistant | Intermediate to advanced | Planned |
| AG-339 | Fleet maintenance assistant | Intermediate to advanced | Planned |
| AG-340 | Warehouse slotting assistant | Intermediate to advanced | Planned |
| AG-341 | Agriculture field observation assistant | Intermediate to advanced | Planned |
| AG-342 | Farm operations planning agent | Intermediate to advanced | Planned |
| AG-343 | Irrigation schedule advisor | Intermediate to advanced | Planned |
| AG-344 | Crop disease literature assistant | Intermediate to advanced | Planned |
| AG-345 | Education tutor workflow | Intermediate to advanced | Planned |
| AG-346 | Learning plan coach | Intermediate to advanced | Planned |
| AG-347 | Course content assistant | Intermediate to advanced | Planned |
| AG-348 | Research grant administration assistant | Intermediate to advanced | Planned |
| AG-349 | Healthcare appointment admin assistant | Intermediate to advanced | Planned |
| AG-350 | Clinical document summarization with review | Intermediate to advanced | Planned |

### Advanced Interfaces and Autonomous Workflows

| ID | Project | Difficulty | Status |
|---|---|---|---|
| AG-351 | Browser research assistant | Advanced | Planned |
| AG-352 | Browser form-filling assistant with approval | Advanced | Planned |
| AG-353 | Browser navigation state tracker | Advanced | Planned |
| AG-354 | Web page change monitor | Advanced | Planned |
| AG-355 | Multi-site comparison agent | Advanced | Planned |
| AG-356 | Accessible browser interaction assistant | Advanced | Planned |
| AG-357 | Screenshot-to-UI explanation agent | Advanced | Planned |
| AG-358 | Visual UI regression investigator | Advanced | Planned |
| AG-359 | Voice conversation agent | Advanced | Planned |
| AG-360 | Speech transcription task agent | Advanced | Planned |
| AG-361 | Voice command intent router | Advanced | Planned |
| AG-362 | Text-to-speech response agent | Advanced | Planned |
| AG-363 | Meeting audio summarizer | Advanced | Planned |
| AG-364 | Call quality analysis assistant | Advanced | Planned |
| AG-365 | Image understanding assistant | Advanced | Planned |
| AG-366 | Chart and diagram interpreter | Advanced | Planned |
| AG-367 | Receipt image extraction agent | Advanced | Planned |
| AG-368 | Product image catalog assistant | Advanced | Planned |
| AG-369 | Video chapter summarizer | Advanced | Planned |
| AG-370 | Video event timeline assistant | Advanced | Planned |
| AG-371 | Multimodal document assistant | Advanced | Planned |
| AG-372 | Audio-video meeting assistant | Advanced | Planned |
| AG-373 | Event-triggered inbox agent | Advanced | Planned |
| AG-374 | Scheduled report generation agent | Advanced | Planned |
| AG-375 | Webhook-triggered workflow agent | Advanced | Planned |
| AG-376 | Email event triage agent | Advanced | Planned |
| AG-377 | Long-running research agent | Advanced | Planned |
| AG-378 | Long-running workflow monitor | Advanced | Planned |
| AG-379 | Background task progress reporter | Advanced | Planned |
| AG-380 | Human takeover browser workflow | Advanced | Planned |
| AG-381 | Agent session handoff manager | Advanced | Planned |
| AG-382 | Cross-session task continuation | Advanced | Planned |
| AG-383 | Personal knowledge assistant | Advanced | Planned |
| AG-384 | Personal task prioritization assistant | Advanced | Planned |
| AG-385 | Daily briefing agent | Advanced | Planned |
| AG-386 | Proactive anomaly notification agent | Advanced | Planned |
| AG-387 | Agentic spreadsheet assistant | Advanced | Planned |
| AG-388 | Presentation research assistant | Advanced | Planned |
| AG-389 | Presentation outline builder | Advanced | Planned |
| AG-390 | Interactive data exploration agent | Advanced | Planned |
| AG-391 | Natural-language dashboard assistant | Advanced | Planned |
| AG-392 | Mobile app task assistant prototype | Advanced | Planned |
| AG-393 | Desktop workflow assistant prototype | Advanced | Planned |
| AG-394 | IoT device monitoring assistant | Advanced | Planned |
| AG-395 | Smart home routine planner | Advanced | Planned |
| AG-396 | Robotics task planner simulator | Advanced | Planned |
| AG-397 | Game-playing strategy agent | Advanced | Planned |
| AG-398 | Simulation environment operator | Advanced | Planned |
| AG-399 | Digital twin query assistant | Advanced | Planned |
| AG-400 | Autonomous workflow sandbox | Advanced | Planned |

### Security, Governance, and Evaluation

| ID | Project | Difficulty | Status |
|---|---|---|---|
| AG-401 | Agent threat modeling assistant | Advanced | Planned |
| AG-402 | Prompt injection test harness | Advanced | Planned |
| AG-403 | Indirect prompt injection evaluator | Advanced | Planned |
| AG-404 | Jailbreak regression suite | Advanced | Planned |
| AG-405 | Tool permission boundary tester | Advanced | Planned |
| AG-406 | Tool argument fuzz tester | Advanced | Planned |
| AG-407 | Tool output poisoning detector | Advanced | Planned |
| AG-408 | Memory poisoning detector | Advanced | Planned |
| AG-409 | Sensitive data redaction middleware | Advanced | Planned |
| AG-410 | PII detection and masking agent | Advanced | Planned |
| AG-411 | Secret leakage scanner for prompts | Advanced | Planned |
| AG-412 | Credential exposure test suite | Advanced | Planned |
| AG-413 | Policy-as-code tool gateway | Advanced | Planned |
| AG-414 | Human approval policy engine | Advanced | Planned |
| AG-415 | High-impact action classifier | Advanced | Planned |
| AG-416 | Least-privilege tool planner | Advanced | Planned |
| AG-417 | Tenant isolation test harness | Advanced | Planned |
| AG-418 | Cross-tenant memory leakage test | Advanced | Planned |
| AG-419 | Agent identity and authorization demo | Advanced | Planned |
| AG-420 | Audit trail integrity verifier | Advanced | Planned |
| AG-421 | Model output schema conformance suite | Advanced | Planned |
| AG-422 | Hallucination evaluation harness | Advanced | Planned |
| AG-423 | Groundedness scoring evaluator | Advanced | Planned |
| AG-424 | Citation correctness evaluator | Advanced | Planned |
| AG-425 | Answer relevance evaluator | Advanced | Planned |
| AG-426 | Retrieval quality benchmark | Advanced | Planned |
| AG-427 | Tool selection accuracy evaluator | Advanced | Planned |
| AG-428 | Tool execution success evaluator | Advanced | Planned |
| AG-429 | Agent task completion evaluator | Advanced | Planned |
| AG-430 | Multi-step trajectory evaluator | Advanced | Planned |
| AG-431 | LLM-as-judge calibration harness | Advanced | Planned |
| AG-432 | Human evaluation review queue | Advanced | Planned |
| AG-433 | Golden dataset regression runner | Advanced | Planned |
| AG-434 | Synthetic task dataset generator | Advanced | Planned |
| AG-435 | Adversarial test case generator | Advanced | Planned |
| AG-436 | Agent red-team scenario runner | Advanced | Planned |
| AG-437 | Model drift monitor | Advanced | Planned |
| AG-438 | Prompt version regression tester | Advanced | Planned |
| AG-439 | Cost and token usage evaluator | Advanced | Planned |
| AG-440 | Latency and throughput benchmark | Advanced | Planned |
| AG-441 | Model comparison benchmark | Advanced | Planned |
| AG-442 | Small-model capability benchmark | Advanced | Planned |
| AG-443 | Fallback behavior test suite | Advanced | Planned |
| AG-444 | Timeout and cancellation test suite | Advanced | Planned |
| AG-445 | Rate limit resilience test suite | Advanced | Planned |
| AG-446 | Data retention policy checker | Advanced | Planned |
| AG-447 | Audit log privacy filter | Advanced | Planned |
| AG-448 | Model risk register generator | Advanced | Planned |
| AG-449 | Agent deployment readiness assessor | Advanced | Planned |
| AG-450 | Agent incident response playbook | Advanced | Planned |

### Research, Knowledge, and Productivity Agents

| ID | Project | Difficulty | Status |
|---|---|---|---|
| AG-451 | Web research planner | Beginner to advanced | Planned |
| AG-452 | Source credibility assessor | Beginner to advanced | Planned |
| AG-453 | Multi-source fact checker | Beginner to advanced | Planned |
| AG-454 | Research question refinement agent | Beginner to advanced | Planned |
| AG-455 | Literature review assistant | Beginner to advanced | Planned |
| AG-456 | Academic paper summarizer | Beginner to advanced | Planned |
| AG-457 | Paper methodology extractor | Beginner to advanced | Planned |
| AG-458 | Citation network explorer | Beginner to advanced | Planned |
| AG-459 | Research gap finder | Beginner to advanced | Planned |
| AG-460 | Experiment design assistant | Beginner to advanced | Planned |
| AG-461 | Hypothesis critique agent | Beginner to advanced | Planned |
| AG-462 | Scientific dataset discovery agent | Beginner to advanced | Planned |
| AG-463 | Patent landscape researcher | Beginner to advanced | Planned |
| AG-464 | Market research assistant | Beginner to advanced | Planned |
| AG-465 | Competitor intelligence monitor | Beginner to advanced | Planned |
| AG-466 | Product requirements analyst | Beginner to advanced | Planned |
| AG-467 | Product discovery interview synthesizer | Beginner to advanced | Planned |
| AG-468 | Customer interview question planner | Beginner to advanced | Planned |
| AG-469 | Survey response analyst | Beginner to advanced | Planned |
| AG-470 | Business report drafter | Beginner to advanced | Planned |
| AG-471 | Executive briefing generator | Beginner to advanced | Planned |
| AG-472 | Policy document comparison assistant | Beginner to advanced | Planned |
| AG-473 | Standards and regulation tracker | Beginner to advanced | Planned |
| AG-474 | Knowledge graph curator | Beginner to advanced | Planned |
| AG-475 | Personal notes search assistant | Beginner to advanced | Planned |
| AG-476 | Knowledge base cleanup agent | Beginner to advanced | Planned |
| AG-477 | Duplicate knowledge detector | Beginner to advanced | Planned |
| AG-478 | Bookmark classification assistant | Beginner to advanced | Planned |
| AG-479 | Reading list curator | Beginner to advanced | Planned |
| AG-480 | Email inbox prioritization assistant | Beginner to advanced | Planned |
| AG-481 | Email thread summarizer | Beginner to advanced | Planned |
| AG-482 | Email reply drafter with approval | Beginner to advanced | Planned |
| AG-483 | Task extraction from messages | Beginner to advanced | Planned |
| AG-484 | Project status report agent | Beginner to advanced | Planned |
| AG-485 | Project risk register assistant | Beginner to advanced | Planned |
| AG-486 | Project plan decomposition agent | Beginner to advanced | Planned |
| AG-487 | Workload prioritization assistant | Beginner to advanced | Planned |
| AG-488 | Focus session planner | Beginner to advanced | Planned |
| AG-489 | Meeting agenda generator | Beginner to advanced | Planned |
| AG-490 | Meeting follow-up assistant | Beginner to advanced | Planned |
| AG-491 | Document comparison assistant | Beginner to advanced | Planned |
| AG-492 | Document quality reviewer | Beginner to advanced | Planned |
| AG-493 | Proposal drafting assistant | Beginner to advanced | Planned |
| AG-494 | RFP response assistant | Beginner to advanced | Planned |
| AG-495 | Grant opportunity finder | Beginner to advanced | Planned |
| AG-496 | Job search research assistant | Beginner to advanced | Planned |
| AG-497 | Job description analyzer | Beginner to advanced | Planned |
| AG-498 | Interview preparation assistant | Beginner to advanced | Planned |
| AG-499 | Learning path planner | Beginner to advanced | Planned |
| AG-500 | Interactive study coach | Beginner to advanced | Planned |
