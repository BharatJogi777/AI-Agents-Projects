# AG-010 — Multi-tool selection agent

**Status:** Modular implementation expanded; tests are authored but not locally executed.  
**Runtime:** Python 3.12+ · **Model:** Ollama `qwen3:4b` by default

## Goal

The model selects from a fixed set of application-owned tools. Python validates arguments and executes handlers. The model cannot add tools, import modules, execute shell commands, or run arbitrary code.

## Architecture

```text
User prompt
   |
   v
MultiToolAgent
   |-- sends tool schemas --> OllamaClient --> Ollama
   |
   <-- structured tool call
   |
   v
Local tool registry
   |-- allowlist lookup
   |-- Pydantic argument validation
   |-- deterministic handler
   v
Tool result message --> model --> final response
```

## Modules

- `multi_tool_agent/registry.py`: typed argument schemas and allowlisted tool implementations.
- `multi_tool_agent/agent.py`: bounded orchestration, validation, dispatch, and tool-result messages.
- `multi_tool_agent/provider.py`: pooled HTTP connection and Ollama response handling.
- `app.py`: compatibility facade.
- `main.py`: CLI entry point.

## Tools included

| Tool | Input | Output |
|---|---|---|
| `add_numbers` | Two finite bounded numbers | Sum |
| `text_length` | Text up to 2,000 characters | Character count |
| `current_utc_time` | Empty object | UTC timestamp |

## Setup and run

```bash
ollama pull qwen3:4b
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
python main.py "Add 12 and 30"
python main.py "How many characters are in agentic systems?"
pytest
```

## Safety and reliability

- Strict schemas reject unexpected arguments.
- Numeric arguments reject NaN/infinity and values outside the configured range.
- Tool names are allowlisted.
- Prompt size and model-step count are bounded.
- Provider timeouts are explicit and error bodies are not exposed to callers.
- Unit tests use a fake model client; provider tests use `httpx.MockTransport`.

## Limitations

This is a local CLI learning project, not a hosted multi-tenant service. It has no authentication, durable run state, per-user quotas, cancellation, or distributed tracing. Tests are committed but have not been run in the maintainer's environment.
