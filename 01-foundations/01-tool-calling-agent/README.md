# 01 — Tool-calling agent

**Difficulty:** Beginner → Intermediate  
**Status:** Expanded reference implementation; tests are authored but not yet executed in a clean environment.  
**Model:** Ollama OpenAI-compatible chat API; default qwen3:4b.

This project demonstrates the complete tool-calling cycle: the model proposes a structured tool call, Python validates and executes an allowlisted function, and the result is returned to the model for a final answer.

## What you will learn

- LLM response vs. an agent loop.
- Tool schemas and model-generated arguments.
- Why the model does not execute Python code.
- Provider adapters and dependency injection.
- Tool allowlists, Pydantic validation, and bounded execution.
- CLI and FastAPI entry points.
- Unit testing without a running model.
- Docker packaging and local Ollama connectivity.
- Trust boundaries and operational gaps.

## Architecture

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

The model proposes an action. Application code validates the tool name and arguments, executes the registered handler, and returns its result. The LLM has no direct Python, shell, filesystem, or database execution access.

Read docs/architecture.md, docs/execution-flow.md, and docs/security.md before running it.

## Prerequisites

- Python 3.12+
- Ollama running on the host
- qwen3:4b or another tool-calling-capable model

    ollama pull qwen3:4b
    ollama list

## Local setup

    python3.12 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -e '.[dev]'
    cp .env.example .env

## Run the CLI

    python -m app.main "What is 19 plus 23? Use a tool to calculate it."
    python -m app.main "What time is it in UTC?"

## Run the HTTP API

    uvicorn app.server:app --host 127.0.0.1 --port 8000

    curl http://127.0.0.1:8000/health/live

    curl -X POST http://127.0.0.1:8000/v1/agent/run \
      -H 'Content-Type: application/json' \
      -d '{"prompt":"What is 19 plus 23? Use a tool."}'

The API factory accepts an injected agent, so endpoint tests do not call Ollama.

## Run with Docker

    docker compose up --build

Ollama remains on the host. Compose binds the API to localhost and uses host.docker.internal for the host Ollama endpoint.

## Run tests

    pytest

Tests use a fake client and should not need Ollama, network access, or a model download. They are authored but must be run locally before this project is marked verified.

## Project layout

    app/
      agent.py             # bounded reasoning/tool loop
      api.py               # FastAPI factory and request boundary
      config.py            # environment-backed settings
      llm.py               # Ollama HTTP adapter
      main.py              # CLI
      server.py            # ASGI entry point
      schemas.py           # API contract
      tools.py             # schemas, validation, allowlist, handlers
      core/                # application error types
      observability/       # structured event interface
    tests/
      test_agent.py
      test_api.py
    docs/
      architecture.md
      execution-flow.md
      security.md

## Current limitations

This is a learning foundation, not a claim of production readiness. The API has no authentication, tenant authorization, rate limiting, durable run store, or distributed tracing. Keep it local or behind a trusted gateway. Add those controls before exposing it to untrusted users. The sample tools are intentionally harmless and have no external side effects.
