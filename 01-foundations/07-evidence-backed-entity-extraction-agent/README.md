# 07 — Evidence-backed Entity Extraction Agent

**Catalogue ID:** AG-007  
**Difficulty:** Beginner → Intermediate  
**Status:** In progress — Ollama integration, deterministic validation, evidence offsets, and tests authored; local execution pending.  
**Runtime:** Python 3.12+  
**Model:** Ollama, default `qwen3:4b`

## Goal

Extract typed entities from unstructured text using an LLM, then verify every returned value against exact source evidence in deterministic application code. The model proposes; Pydantic and the evidence verifier decide what is accepted.

## Architecture

```text
CLI request -> extraction agent -> JSON-encode untrusted source
    -> Ollama native /api/chat + JSON Schema
    -> Pydantic strict schema + duplicate validation
    -> EvidenceVerifier
       -> exact evidence substring
       -> entity value inside evidence
       -> source and entity character offsets
       -> SHA-256 source fingerprint
    -> verified extraction response
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

Override model or endpoint:

```bash
OLLAMA_MODEL=qwen3:4b OLLAMA_BASE_URL=http://localhost:11434 \
  python -m app.main "Acme launched Product Atlas in Singapore."
```

Output includes entities, exact evidence, source offsets, and a SHA-256 fingerprint of the source string. Offsets are zero-based Python Unicode code-point offsets, not UTF-8 byte or JavaScript UTF-16 offsets.

## Test without Ollama

```bash
pytest
```

Tests use a fake structured generator and require no model server or credentials.

## Supported entity types

person, organization, product, service, location, date_or_time, identifier.

## Trust boundary

Evidence must be an exact substring of the source; entity values must occur within their evidence quote. Unknown fields, invalid types, malformed JSON, duplicate entities, empty input, and oversized input are rejected. These checks do not prove semantic correctness, extraction completeness, or that a genuine quote supports the intended interpretation. Use evaluation data and human review for high-impact use cases.

## Operational boundaries

- One source per request; no persistence or batch API.
- No automatic repair/retry; invalid output fails explicitly (see AG-008).
- Input/output payloads have configurable byte limits.
- Uses Ollama native `/api/chat` and JSON Schema `format`.
- JSON-string prompt framing helps avoid delimiter-breaking input but is not a complete prompt-injection defense.
- Do not log source documents or full model outputs by default; they may contain sensitive data.
