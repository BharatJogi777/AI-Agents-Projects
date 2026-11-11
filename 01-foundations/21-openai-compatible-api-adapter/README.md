# AG-021 — OpenAI-compatible API adapter

A non-streaming chat-completions adapter for OpenAI-compatible endpoints. It maps normalized messages and generation options, sends bearer credentials, validates response structure and usage, and reuses a connection-pooled HTTPX client.

## Architecture
- `openai_adapter/contracts.py`: validated request/message/response DTOs.
- `openai_adapter/provider.py`: HTTP lifecycle, endpoint mapping, auth header, response validation, and sanitized provider errors.
- `app.py`: compatibility facade.

## Run
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Pass the API root (including `/v1` where required). This adapter intentionally supports plain non-streaming text only. Vendor differences in token limits, tool calls, JSON mode, and errors require explicit capabilities. Tests are authored; local execution remains pending.
