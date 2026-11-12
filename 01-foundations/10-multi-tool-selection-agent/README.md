# AG-010 — Multi-tool selection agent

**Status:** Expanded modular implementation; tests are authored but have not been executed in the maintainer's environment.  
**Runtime:** Python 3.12+ · **Local model:** Ollama `qwen3:4b`

## What this project demonstrates

A model can choose among multiple application-owned tools in one turn. The model proposes a tool name and arguments; the Python application validates the request against a fixed registry and executes the handler. The model never gets direct Python, shell, filesystem, or network execution privileges.

## Architecture

```text
CLI
 └── MultiToolAgent
      ├── OllamaClient (HTTPX connection pool)
      ├── bounded model/tool loop
      ├── tool-call count + ID validation
      └── local registry
           ├── Pydantic argument schema
           ├── allowlisted handler
           └── bounded JSON result
```

## Project structure

```text
10-multi-tool-selection-agent/
├── multi_tool_agent/
│   ├── __init__.py
│   ├── agent.py          # orchestration, limits, dispatch boundary
│   ├── provider.py       # Ollama HTTP adapter
│   └── registry.py      # schemas and deterministic tool handlers
├── tests/
│   ├── test_agent.py
│   └── test_provider.py
├── app.py               # compatibility exports
├── main.py              # CLI lifecycle
├── pyproject.toml
└── README.md
```

## Available tools

| Tool | Arguments | Purpose |
|---|---|---|
| `add_numbers` | `a`, `b` | Add finite, bounded numbers |
| `text_length` | `text` | Count Unicode code points and UTF-8 bytes |
| `current_time` | `timezone` (defaults to UTC) | Return time in a validated IANA timezone |

The tools are deterministic application capabilities, except that `current_time` intentionally reads the system clock. No tool is registered dynamically from model output.

## Run locally

Ollama must be running on the host and the model must be available:

```bash
ollama pull qwen3:4b
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python main.py "Add 12 and 30"
python main.py "Count the characters in agentic systems"
python main.py "What time is it in Asia/Kolkata?"
pytest
```

If Ollama uses another address or model:

```bash
python main.py --base-url http://localhost:11434 --model qwen3:4b "Add 7 and 9"
```

## Safety and reliability boundaries

- Tool names are resolved only from a local allowlist.
- Pydantic schemas reject unknown fields and invalid values.
- A run has bounded model steps, tool calls per step, prompt bytes, tool-result bytes, and final-answer bytes.
- Tool-call IDs are checked for duplicates and copied to corresponding tool-result messages when supplied.
- Invalid arguments produce a generic error; submitted values are not echoed into diagnostics.
- Provider timeouts are explicit and HTTP response bodies are not leaked.
- The model's tool output is treated as untrusted data. Tool output must never itself authorize a privileged action.

## Tests

The test suite uses fake model responses and HTTPX MockTransport; it does not require a live Ollama server. The tests are committed but have **not** been run in the maintainer's environment. Run `pytest` locally after installation.

## Production gaps

This is a local learning CLI, not a hosted multi-tenant agent service. It does not include authentication, durable run state, tenant isolation, quotas, cancellation, distributed tracing, or a human-approval workflow. A production deployment should add those controls around the same registry boundary and should separately authorize every consequential tool action.
