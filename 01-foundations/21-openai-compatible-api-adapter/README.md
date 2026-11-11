# AG-021 — OpenAI-compatible API adapter

A minimal non-streaming adapter for servers exposing the OpenAI chat-completions shape. It normalizes messages, generation settings, finish reason, and token usage; API keys are sent as bearer credentials and never included in error messages.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Configure the provider API root, including its `/v1` prefix where applicable. Compatibility varies: tool calling, structured output, token limits, and error formats differ by vendor. This adapter intentionally supports plain text only. Tests are authored but not yet executed.
