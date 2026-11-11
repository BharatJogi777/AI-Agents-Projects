# AG-020 — Ollama local model adapter

Implements a concrete Ollama `/api/chat` provider for a small provider-neutral text-chat contract. It maps messages and generation options, exposes health/model-list operations, validates response shape, maps token usage, and wraps transport/provider failures in a stable exception.

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

provider = OllamaProvider()
request = ChatRequest((ChatMessage("user", "Explain tool calling briefly"),), "qwen3:4b")
print(provider.chat(request).content)
```

The adapter currently implements non-streaming text chat only. Ollama tool calling, structured output, vision, and streaming need separate explicit capabilities. The default URL targets a local Ollama service; use an explicit reachable URL in container deployments. Local test execution and live Ollama integration are pending.
