# AG-020 — Ollama local model adapter

A concrete Ollama `/api/chat` implementation of the provider-neutral text-chat contract. It uses a persistent HTTPX client with connection pooling, maps chat options, checks health, lists models, validates response fields, and normalizes token usage.

## Architecture
- `contracts.py`: minimal request/response DTOs retained for compatibility with the original tutorial.
- `ollama_adapter/provider.py`: HTTP lifecycle, transport mapping, response validation, health/model-list operations, and sanitized provider errors.
- `app.py`: compatibility facade.

## Run

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
ollama pull qwen3:4b
pytest
```

Example:

```python
from app import OllamaProvider
from contracts import ChatMessage, ChatRequest

with OllamaProvider() as provider:
    request = ChatRequest((ChatMessage("user", "Explain tool calling briefly"),), "qwen3:4b")
    print(provider.chat(request).content)
```

The adapter implements non-streaming text chat only. Tool calling, structured output, vision, and streaming need separate explicit capabilities. For container deployments, configure a reachable Ollama URL. Tests are authored; local execution and live Ollama integration remain pending.
