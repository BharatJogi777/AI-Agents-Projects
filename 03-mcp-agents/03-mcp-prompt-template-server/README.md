# AG-103 — MCP prompt-template server

This project exposes reusable, parameterized prompt templates through the MCP prompts capability. It keeps prompt construction deterministic and validates user-supplied fields before they enter the template.

## Learning objectives

- Register a prompt with the MCP Python SDK.
- Define typed prompt arguments and sensible defaults.
- Validate and normalize user input in a separate application service.
- Keep prompt content separate from transport registration.
- Test generated prompt text without launching an MCP host.

## Setup

Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

## Run

```bash
python -m app.server
```

The server communicates over stdio. Configure it in an MCP host as a child process; do not use stdout for diagnostic logging.

## Prompt contract

Prompt name: `technical_brief`

Arguments:
- `topic` — required, 3–120 characters.
- `audience` — optional; one of `beginner`, `intermediate`, or `expert`.
- `include_examples` — optional boolean, defaults to true.

The generated prompt asks the model to explain the topic at the selected level and to distinguish established facts from assumptions. This server does not call a model or execute the resulting instructions.

## Architecture

```text
MCP host
  | prompts/list + prompts/get
  v
app.server (FastMCP prompt adapter)
  |
  v
app.services.prompt_templates (validation + rendering)
```

## Safety

Prompt arguments are untrusted input. Length and enum validation constrain the template fields, but prompt text is not a security boundary. A consuming agent must still apply its own system policy, tool permissions, and output validation. Never place credentials or private data in reusable prompt templates.

## Tests

```bash
pytest
```

Tests cover defaults, formatting, invalid audience values, and malformed topics.
