# 08 — Schema Repair and Retry Agent

**Catalogue ID:** AG-008  
**Difficulty:** Beginner → Intermediate  
**Status:** In progress — implementation and deterministic tests committed; local execution pending.  
**Runtime:** Python 3.12+  
**Model:** Ollama, default `qwen3:4b`

## Goal

Generate a typed `TaskReport` from a work request. If the model returns malformed JSON or data that violates the strict Pydantic contract, send bounded validation feedback and request a corrected response.

AG-002 demonstrates strict structured output and fail-fast validation. AG-008 adds a bounded repair state machine, explicit retry classification, input/output size limits, and safe operational boundaries.

## Architecture

| Component | Responsibility |
|---|---|
| `app/schemas.py` | Strict Pydantic response contract and nested action-item schema |
| `app/agent.py` | Generation → validation → repair loop and attempt metadata |
| `app/llm.py` | Persistent HTTPX adapter for Ollama's native JSON Schema mode |
| `app/main.py` | CLI composition, configuration and deterministic client cleanup |
| `tests/` | Fake-generator state-machine tests and HTTP adapter tests |

## Execution flow

1. Validate the request and enforce a UTF-8 byte limit before calling the model.
2. JSON-encode the request so embedded quotes or delimiter-like text cannot escape the data boundary.
3. Send the Pydantic JSON Schema to Ollama's `/api/chat` endpoint using `format`.
4. Enforce character and UTF-8 byte limits on the returned content.
5. Validate strictly. Unknown fields and type coercion are rejected.
6. On output-contract failure only, send bounded field-level feedback and the bounded rejected response as untrusted conversation data.
7. Return a typed report or raise `SchemaRepairExhausted`. Never return the last invalid payload.

## Setup

```bash
ollama pull qwen3:4b
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

## Run

```bash
python -m app.main "Checkout API latency increased after deployment. The on-call engineer should inspect metrics."
```

Configure the maximum number of repairs (not counting the initial generation):

```bash
python -m app.main --max-retries 1 "Investigate elevated API latency."
```

The default is two repairs; allowed values are 0–3. The final JSON is printed to stdout, while attempt metadata is written to stderr. Set `OLLAMA_BASE_URL` and `OLLAMA_MODEL` to override the local defaults.

## Test without Ollama

```bash
pytest
```

Tests use deterministic fake generators and HTTPX mock transports; no model server or API key is required.

## Retry and security boundaries

- Only malformed/schema-invalid, empty, or oversized model output triggers repair.
- Network, timeout, HTTP, and provider failures propagate immediately. Retrying these as schema failures would amplify outages.
- The retry count is capped at three; no unbounded loop or network backoff is hidden in this component.
- Validation feedback excludes submitted field values and is bounded by count and size.
- The original request is JSON-encoded. This is safer framing, not a prompt-injection defence.
- Rejected model output is included only as bounded untrusted conversation data. Never use model output as authorization or tool permission.
- Logs contain attempt metadata, not request text or raw model output.
- The Ollama HTTP client is closed by the CLI even when generation fails.

## Limitations

A schema-valid response can still be factually wrong or incomplete. Repair is not grounding. Add source evidence checks, semantic evaluation, rate limits, metrics, tracing, and human review before using outputs for consequential decisions.
