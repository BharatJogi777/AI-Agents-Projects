# 07 — Evidence-backed Entity Extraction Agent

**Catalogue ID:** AG-007  
**Difficulty:** Beginner → Intermediate  
**Status:** In progress — implementation and deterministic tests committed; local execution pending.  
**Runtime:** Python 3.12+  
**Model:** Ollama, default `qwen3:4b`

## Goal

Extract typed entities from unstructured text while requiring an exact evidence quote for every extracted value. The model proposes structured data; Pydantic and deterministic source checks decide whether the result is accepted.

This is intentionally different from AG-002: AG-002 classifies a work request into a task-analysis object; AG-007 extracts multiple source-grounded entities and verifies evidence against the original input.

## Architecture

```text
Source text
    |
    v
Ollama JSON Schema generation
    |
    v
Pydantic strict schema validation
    |
    v
Evidence substring validation
    |
    +-- valid --> typed ExtractionResult
    |
    +-- invalid -> ExtractionValidationError
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
python -m app.main "Bharat deployed the Checkout API in Bengaluru on 12 November 2026."
```

Override the model or endpoint:

```bash
OLLAMA_MODEL=qwen3:4b OLLAMA_BASE_URL=http://localhost:11434 \
  python -m app.main "Acme launched Product Atlas in Singapore."
```

## Test without Ollama

```bash
pytest
```

The tests use a fake generator and require no model server or API credentials.

## Supported entity types

- person
- organization
- product
- service
- location
- date_or_time
- identifier

## Trust boundary

Every entity must include an evidence string that is an exact substring of the supplied source. The entity value must itself occur in that evidence. Duplicate entities, unknown fields, invalid types, malformed JSON, empty input, and oversized input are rejected.

This is a useful grounding check, not a proof of semantic correctness. A model can still choose an incorrect type or omit entities. Use an evaluation dataset and human review for high-impact extraction. Exact substring matching is deliberately conservative and may reject normalized dates, aliases, or paraphrased evidence.

## Limitations

- One source document per request; no batch API or persistence.
- No automatic repair/retry. Invalid results fail explicitly.
- Character input limit is 20,000; tune it alongside the model context budget.
- The bundled client uses Ollama's native `/api/chat` endpoint and JSON Schema `format`.
- The application does not claim completeness or factual correctness beyond its deterministic evidence checks.
