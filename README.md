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
