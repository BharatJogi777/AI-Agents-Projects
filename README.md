# AI Agents Projects

A hands-on engineering collection of AI agents: from first principles to reliable, observable, secure systems.

This repository is being built as an implementation-first alternative to collections that primarily catalogue agent ideas or link to external projects. The goal is to cover 500+ agent patterns and use cases over time, while only marking a project complete when its implementation, tests, and documentation meet the repository standard.

> **Status:** Foundation and audit phase. Projects are added incrementally; planned projects are not represented as completed.

## What you will find

- **Foundations:** LLM calls, structured output, tool calling, state, memory, retries, and agent loops.
- **RAG agents:** document ingestion, retrieval, citations, SQL/data assistants, and evaluation.
- **MCP agents:** MCP servers, clients, tool discovery, multiple servers, authorization, and failure handling.
- **Orchestration:** planning, routing, reflection, supervisor-worker, human approval, and multi-agent workflows.
- **Engineering agents:** code review, debugging, test generation, documentation, and repository maintenance.
- **Operations agents:** log investigation, incident response, cloud and Kubernetes operations.
- **Domain agents:** support, research, analytics, education, healthcare administration, finance workflows, logistics, and agriculture.
- **Advanced systems:** browser automation, voice interfaces, long-running workflows, and agent evaluation.

## Engineering principles

1. Runnable code beats screenshots and pseudo-code.
2. A model proposes; deterministic application code validates and executes.
3. Tools use explicit schemas, bounded permissions, timeouts, and auditable results.
4. State and memory are explicit, scoped, and inspectable.
5. Every project includes tests for its important behavior and failure paths.
6. Secrets are never committed; configuration is documented through safe examples.
7. Human approval is required for consequential or irreversible actions.
8. Model/provider/framework choices are isolated behind adapters where useful.
9. Claims of production readiness require evidence: tests, security controls, observability, and operational documentation.
10. Small local models (including Ollama) are supported when practical; cloud models are optional alternatives.

## Repository map

| Area | Purpose |
|---|---|
| `01-foundations/` | Core agent concepts and minimal working agents |
| `02-rag-agents/` | Retrieval-augmented agents |
| `03-mcp-agents/` | MCP clients, servers, and integrations |
| `04-orchestration/` | Stateful and multi-agent workflows |
| `05-developer-agents/` | Software engineering agents |
| `06-devops-agents/` | Infrastructure and incident agents |
| `07-domain-agents/` | Business and industry use cases |
| `08-advanced-agents/` | Advanced interfaces and autonomous workflows |
| `shared/` | Reusable libraries only when abstractions are genuinely shared |
| `docs/` | Architecture, standards, roadmap, and learning guides |

See [the roadmap](docs/ROADMAP.md) and [project implementation standard](docs/PROJECT_STANDARD.md).

## Project maturity

Projects use these labels:

- **Planned:** idea is recorded; no implementation claim.
- **In progress:** implementation is actively being built.
- **Implemented:** main flow runs and basic tests pass.
- **Verified:** tests include important failure cases; setup is reproducible.
- **Production-oriented:** security, observability, deployment, limits, and operational guidance are included and tested where feasible.

A project is never labelled production-ready merely because it uses an agent framework.

## Local development

Python 3.12+ is the default for new Python projects unless a framework has a documented compatibility constraint. Each project will provide its own setup instructions and dependency lock or pinned requirements.

Typical workflow:

```bash
git clone https://github.com/BharatJogi777/AI-Agents-Projects.git
cd AI-Agents-Projects
```

Then follow the README inside the selected project. Do not install every project's dependencies into one global environment.

## Hardware and model guidance

The default development path should work on a modest developer machine where possible. Ollama can be used for local inference; cloud APIs must be optional unless a project explicitly teaches a provider-specific integration. Document expected RAM, model size, latency trade-offs, and any external API cost.

## Safety

Agents must not receive unrestricted shell, filesystem, database, browser, or cloud access. Use least-privilege tools, input validation, allowlists, execution limits, approval gates, and audit logs. Treat retrieved documents and tool outputs as untrusted data.

## Reference material and attribution

The repository is informed by public agent projects and learning resources, including [500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects). This repository is an independent implementation effort, not a mirror. External code or assets will only be incorporated when their licences permit it and attribution requirements are met.

## Contributing

Contributions should follow [PROJECT_STANDARD.md](docs/PROJECT_STANDARD.md). Every new project needs a clear use case, architecture, setup, runnable example, tests, limitations, and security notes.

## License

A repository licence will be selected and added before external contributions or code reuse. Individual third-party components retain their original licences and notices.
