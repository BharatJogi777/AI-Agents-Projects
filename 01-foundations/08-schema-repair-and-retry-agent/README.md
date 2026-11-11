# 08 — Schema Repair and Retry Agent

**Catalogue ID:** AG-008  
**Difficulty:** Beginner → Intermediate  
**Status:** In progress — implementation and deterministic tests committed; local execution pending.  
**Runtime:** Python 3.12+  
**Model:** Ollama, default `qwen3:4b`

## Goal

Generate a typed `TaskReport` from a work request. If the model returns malformed JSON or data that violates the Pydantic contract, send bounded validation feedback and ask for a corrected response.

AG-002 demonstrates strict structured output and fail-fast validation. AG-008 adds a deliberately bounded repair loop.

## Flow

```text
User request
    |
    v
LLM structured JSON generation
    |
    v
Pydantic strict validation
    |
    +-- valid --> return typed result + attempt metadata
    |
    +-- invalid --> bounded validation feedback
                      |
                      v
                 repair request
                      |
                      +---- retry (up to configured limit)
                      |
                      +---- exhausted -> explicit error
```

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
``

The default is two repairs; allowed values are 0–3. The final JSON is printed to stdout, while attempt metadata is written to stderr.

## Test without Ollama

```bash
pytest
```

Tests use a deterministic fake generator, so no model server or API key is required.

## Reliability boundaries

- Only schema/empty/oversized output failures trigger repair. Network and provider errors propagate immediately; repeating them as if they were JSON errors wastes time and can amplify outages.
- Retry count is capped at three. There is no unbounded loop.
- Validation feedback includes bounded field paths and messages, not rejected field values.
- Invalid model output is treated as untrusted data and never promoted to system instructions.
- The raw response included in the repair conversation is capped.
- If repair attempts are exhausted, the application raises `SchemaRepairExhausted`; it never returns the last invalid payload.

## Limitations

A schema-valid response can still be factually wrong or incomplete. Repair is not a grounding mechanism. Add source evidence checks, evaluation data, rate limits, telemetry, and human review before using extracted data for consequential decisions.
