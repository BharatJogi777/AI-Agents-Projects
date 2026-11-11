# 01 — Structured Output Agent

**Difficulty:** Beginner → Intermediate  
**Status:** In progress — implementation and deterministic tests committed; local Ollama execution still needs verification.  
**Model:** Ollama native chat API, default `qwen3:4b`  
**Validation:** Pydantic v2

## What it does

Takes a plain-language work request and returns a validated `TaskAnalysis` object containing:

- A concise summary.
- A controlled priority enum.
- A controlled category enum.
- Typed action items.
- A human-review flag.
- An uncertainty field instead of invented facts.

Ollama is given the Pydantic-generated JSON Schema through its native `/api/chat` `format` field. The application then independently validates the returned content with Pydantic. Model-side constrained generation is useful, but application-side validation remains mandatory.

## Architecture

```text
User text
   |
   v
StructuredOutputAgent
   | build JSON Schema from TaskAnalysis
   v
OllamaClient -----> Ollama /api/chat (format: JSON Schema)
   |                         |
   |<------ JSON text --------+
   v
Pydantic model_validate_json(strict=True)
   |
   +---- valid ----> TaskAnalysis object ----> JSON output
   |
   +---- invalid --> OutputValidationError
```

## Prerequisites

- Python 3.12+
- Ollama installed and running
- A model that supports structured output, such as `qwen3:4b`

```bash
ollama pull qwen3:4b
```

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
cp .env.example .env
```

## Run

```bash
python -m app.main "Checkout API latency increased after the latest deployment. The on-call engineer should inspect metrics."
```

Expected output shape (illustrative; model-generated wording can differ):

```json
{
  "summary": "Investigate elevated API latency affecting checkout requests.",
  "priority": "high",
  "category": "operations",
  "action_items": [
    {
      "task": "Inspect API latency metrics and recent deployments",
      "owner": null,
      "due_date": null
    }
  ],
  "needs_human_review": true,
  "uncertainty": "The affected time window and customer impact are not specified."
}
```

The agent must not invent an owner or deadline when none was provided.

## Run tests without Ollama

```bash
pytest
```

The tests use a fake structured-output generator and require no API key or running model server.

## Why both JSON Schema and Pydantic?

- **JSON Schema at generation time:** guides the model toward the required shape and allowed values.
- **Pydantic at the application boundary:** rejects malformed JSON, unknown fields, invalid enums, and values outside the declared constraints.
- **Business logic after validation:** should consume the typed `TaskAnalysis`, not raw model text.

Never assume that a valid JSON document is automatically correct or factually grounded. Schema validation checks shape and types, not truth.

## Limitations and next improvements

- No automatic retry or repair is performed; invalid output fails explicitly.
- This project does not verify factual correctness against source documents.
- The example is a CLI, not a multi-user API.
- Before production use, add request limits, authentication, metrics, tracing, and an evaluation dataset.
- If a model or Ollama version does not support the supplied schema, the request may fail; verify model compatibility rather than silently accepting unconstrained text.
