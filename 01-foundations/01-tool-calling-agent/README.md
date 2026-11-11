# 01 — Tool-calling agent

**Difficulty:** Beginner → Intermediate  
**Status:** Expanded reference implementation; automated tests are authored but have not been run in the maintainer's local environment.  
**Model:** Ollama OpenAI-compatible chat API; default `qwen3:4b`.

This project demonstrates the complete tool-calling cycle: the model proposes a structured tool call, Python validates and executes an allowlisted function, and the result is returned to the model for a final answer.

## What you will learn

- LLM response vs. an agent loop.
- Tool schemas and model-generated arguments.
- Why the model does not execute Python code.
- Provider adapters and dependency injection.
- Tool allowlists, Pydantic validation, and bounded execution.
- CLI and FastAPI entry points.
- Liveness vs. dependency-aware readiness.
- Reusable HTTP connections and provider error normalization.
- Unit testing without a running model.
- Docker packaging and local Ollama connectivity.

## Architecture

```text
CLI / HTTP API
      |
      v
ToolCallingAgent ---- ChatClient protocol
      |                       |
      |                 OllamaChatClient
      |                       |
      v                       v
Tool allowlist            Ollama API
      |
      v
Pydantic validation
      |
      v
Deterministic Python handlers
```

The model proposes an action. Application code validates the tool name and arguments, executes the registered handler, and returns its result. The LLM has no direct Python, shell, filesystem, or database execution access.

Read `docs/architecture.md`, `docs/execution-flow.md`, and `docs/security.md` before running it.

## Prerequisites

- Python 3.12+
- Ollama running on the host
- `qwen3:4b` or another tool-calling-capable model

```bash
ollama pull qwen3:4b
ollama list
```

## Local setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
cp .env.example .env
```

## Run the CLI

```bash
python -m app.main "What is 19 plus 23? Use a tool to calculate it."
python -m app.main "What time is it in UTC?"
```

## Run the HTTP API

```bash
uvicorn app.server:app --host 127.0.0.1 --port 8000
curl http://127.0.0.1:8000/health/live
curl http://127.0.0.1:8000/health/ready
curl -X POST http://127.0.0.1:8000/v1/agent/run \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"What is 19 plus 23? Use a tool."}'
```

- `/health/live` reports process health only.
- `/health/ready` checks that Ollama responds and the configured model is installed. It does not execute a completion.
- The API factory accepts injected dependencies, so endpoint tests do not call Ollama.

## Run with Docker

```bash
docker compose up --build
```

Ollama remains on the host. Compose binds the API to localhost and uses `host.docker.internal` for the host Ollama endpoint.

## Run tests

```bash
pytest
```

Tests use fake clients and `httpx.MockTransport`; the default test suite does not need Ollama, network access, or a model download. Tests are authored but must be run locally before this project is marked verified.

## Project layout

```text
app/
  agent.py             # bounded reasoning/tool loop
  api.py               # FastAPI factory and request boundary
  config.py            # environment-backed settings
  llm.py               # Ollama HTTP adapter and readiness check
  main.py              # CLI composition root
  server.py            # ASGI composition root
  schemas.py            # reusable API contract models
  tools.py             # tool schemas, allowlist, validation, handlers
  core/                # application error types
  observability/       # structured event interface
tests/
  test_agent.py
  test_api.py
  test_llm.py
docs/
  architecture.md
  execution-flow.md
  security.md
```

## Current limitations

This is a learning foundation, not a claim of production readiness. The API has no authentication, tenant authorization, rate limiting, durable run store, cancellation endpoint, or distributed tracing. Provider calls are synchronous and FastAPI runs the synchronous route in its worker thread pool. Keep it local or behind a trusted gateway. The sample tools are intentionally harmless and have no external side effects.
