# 01 — Tool-calling agent

**Difficulty:** Beginner → Intermediate  
**Status:** Implemented (automated tests authored; local Ollama integration still needs verification)  
**Model:** Ollama through its OpenAI-compatible API  
**Default model:** `qwen3:4b`

A small agent that receives a user request, lets the model choose from a strict allowlist of tools, validates tool arguments, executes deterministic Python functions, returns tool results to the model, and produces a final answer.

## What this teaches

- The difference between an LLM response and an agent loop.
- How tool schemas are exposed to a model.
- Why the model proposes a tool call but application code executes it.
- How tool results are added back to the conversation.
- Why tool allowlists, schema validation, and maximum step limits matter.
- How to test an agent without making paid model calls.

## Architecture

```text
User prompt
    |
    v
ToolCallingAgent -----> OllamaChatClient -----> Ollama /v1/chat/completions
    |                           ^
    | model proposes tool call  | tool result + conversation
    v                           |
Allowlist + Pydantic validation |
    |
    v
Deterministic Python tool
    |
    +---- add_numbers
    +---- get_current_utc_time
```

The LLM never executes Python code. It returns a structured request. The application checks the tool name and arguments, runs an allowlisted function, and sends the result back to the model.

## Prerequisites

- Python 3.12+
- Ollama installed and running on the host
- A tool-capable local model, for example `qwen3:4b`

Pull the model if needed:

```bash
ollama pull qwen3:4b
ollama list
```

## Setup

From this directory:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
cp .env.example .env
```

Edit `.env` only if you need a different model or Ollama endpoint.

## Run

```bash
python -m app.main "What is 19 plus 23? Use a tool to calculate it."
python -m app.main "What time is it in UTC?"
```

Ollama's OpenAI-compatible endpoint is expected at `http://localhost:11434/v1/chat/completions`.

## Test without Ollama

```bash
pytest
```

Tests use a fake model client, so they do not need an API key, internet access, or a running Ollama service.

## Safety and current limitations

- Only `add_numbers` and `get_current_utc_time` are registered.
- Unknown tools are rejected.
- Arguments are validated before execution.
- The number of model steps is bounded.
- The example has no shell, filesystem, browser, database, or network tools.
- This is a teaching foundation, not a deployed multi-user service. Before exposing it as an API, add authentication, rate limits, per-user budgets, request IDs, structured audit events, and concurrency controls.
- Model behavior varies. If the model does not produce a tool call, inspect its response and confirm that the selected model supports tool calling.

## Project structure

```text
app/
  agent.py       # bounded agent loop
  config.py      # environment-backed settings
  llm.py         # Ollama API adapter
  main.py        # CLI
  tools.py       # tool schemas, validation, allowlist
tests/
  test_agent.py  # deterministic unit tests
```
