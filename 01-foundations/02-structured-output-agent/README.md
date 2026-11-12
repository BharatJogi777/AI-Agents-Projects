# 02 — Structured-output agent

**Difficulty:** Beginner → Intermediate  
**Status:** Expanded implementation; tests are authored but local execution and live Ollama compatibility still need verification.  
**Model:** Ollama native chat API, default `qwen3:4b`  
**Validation:** Pydantic v2 plus exact source-evidence checks

## What it does

Takes a plain-language work request and returns a validated `TaskAnalysis` object containing a summary, controlled priority and category, typed action items, a human-review flag, and uncertainty. Every action item must include an exact quote from the source request. Extracted owners and due dates must each have their own exact supporting quote.

The model can still produce an inaccurate summary or classification. Evidence checks reduce unsupported extraction; they do not prove that the model's interpretation is correct.

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
       exact source-substring validation
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
python -m app.main "Checkout API latency increased. Alice will inspect the metrics."
pytest
```

The deterministic tests use a fake generator and an `httpx.MockTransport` adapter. They do not require a running Ollama service or model download. Tests are authored but have not been executed in the maintainer's environment.

## Why both JSON Schema and Pydantic?

- **JSON Schema at generation time:** guides the model toward the required shape and allowed values.
- **Pydantic at the application boundary:** rejects malformed JSON, unknown fields, invalid enums, and values outside declared constraints.
- **Exact evidence validation:** verifies that evidence quotes are literal substrings of the original input and that extracted owners/dates occur in their own evidence quote.
- **Business logic after validation:** consumes the typed `TaskAnalysis`, not raw model text.

Schema validation checks shape and types, not truth. Exact quote validation checks provenance, not whether the model's classification or interpretation is correct.

## Project layout

```text
app/
  agent.py       # orchestration, limits, schema and source-evidence validation
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
- Exact substring evidence can be overly strict for paraphrases and multilingual normalization.
- Factual correctness of summaries, priority, and category is not guaranteed.
- This is a CLI teaching project, not a multi-tenant service.
- Add authentication, rate limits, metrics, tracing, and an evaluation dataset before exposing it as a service.
