# 02 — Structured-output agent

**Difficulty:** Beginner → Intermediate  
**Status:** Expanded implementation; tests are authored but local execution and live Ollama compatibility still need verification.  
**Model:** Ollama native chat API, default `qwen3:4b`  
**Validation:** Pydantic v2

## What it does

Takes a plain-language work request and returns a validated `TaskAnalysis` object containing a summary, controlled priority and category, typed action items, a human-review flag, and uncertainty. The model must not invent an owner or deadline when the source does not provide one.

Ollama receives the Pydantic-generated JSON Schema through its native `/api/chat` `format` field. The application independently validates the returned content with Pydantic. Model-side constrained generation is useful, but application-side validation remains mandatory.

## Architecture

```text
CLI -> StructuredOutputAgent -> StructuredGenerator protocol
             |                           |
             |                     OllamaClient
             |                           |
             |                     Ollama /api/chat
             |                           |
             +<------ JSON text ----------+
             |
       output byte limit
             |
       strict Pydantic validation
             |
       TaskAnalysis object
```

## Prerequisites and setup

- Python 3.12+
- Ollama running locally
- A model supporting structured output, such as `qwen3:4b`

```bash
ollama pull qwen3:4b
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
cp .env.example .env
```

## Run

```bash
python -m app.main "Checkout API latency increased after the latest deployment. The on-call engineer should inspect metrics."
pytest
```

The deterministic tests use a fake generator and an `httpx.MockTransport` adapter. They do not require a running Ollama service or model download. Tests are authored but have not been executed in the maintainer's environment.

## Why both JSON Schema and Pydantic?

- **JSON Schema at generation time:** guides the model toward the required shape and allowed values.
- **Pydantic at the application boundary:** rejects malformed JSON, unknown fields, invalid enums, and values outside declared constraints.
- **Business logic after validation:** consumes the typed `TaskAnalysis`, not raw model text.

Schema validation checks shape and types, not truth. Do not treat a valid JSON object as factual evidence.

## Project layout

```text
app/
  agent.py       # orchestration, input/output limits, strict validation
  config.py      # environment-backed settings
  llm.py         # Ollama HTTP adapter
  main.py        # CLI composition root
  schemas.py     # Pydantic output contract
tests/
  test_agent.py
  test_llm.py
docs/
  architecture.md
```

## Limitations

- Invalid output fails explicitly; no automatic repair loop is performed.
- Factual correctness is not verified against source documents.
- This is a CLI teaching project, not a multi-tenant service.
- Add authentication, rate limits, metrics, tracing, and an evaluation dataset before exposing it as a service.
