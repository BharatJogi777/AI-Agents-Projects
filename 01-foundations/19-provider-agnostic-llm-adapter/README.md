# AG-019 — Provider-agnostic LLM adapter

A provider-neutral boundary for non-streaming text chat. Agent/business logic builds a normalized request and calls `LLMClient`; concrete adapters translate it to Ollama, an OpenAI-compatible API, or another backend and translate responses back.

## Architecture

- `llm_adapter/contracts.py`: immutable request/message/response contracts with bounded JSON metadata.
- `llm_adapter/provider.py`: provider protocol, defensive registry, explicit provider selection, response contract enforcement.
- `llm_adapter/errors.py`: normalized provider error taxonomy and retryability metadata.
- `app.py`: compatibility facade.
- `tests/test_adapter.py`: routing, validation, immutability, and error contract tests.

## Usage

```python
from llm_adapter import ChatMessage, ChatRequest, LLMClient

request = ChatRequest(
    messages=(ChatMessage("user", "Explain vector search"),),
    model="qwen3:4b",
    temperature=0.2,
    max_tokens=512,
)
client = LLMClient(
    providers={"local": ollama_adapter, "remote": openai_compatible_adapter},
    default_provider="local",
)
response = client.chat(request)
print(response.content)
```

The provider objects above are implementations you supply. This project defines the contract, not concrete network clients.

## Adapter responsibilities

Each concrete adapter must map messages and generation settings, configure connection/read/total timeouts and response-size limits, parse responses defensively, and translate vendor errors into `llm_adapter.errors` types. Never expose API keys, authorization headers, raw request bodies, or sensitive diagnostics in exceptions.

## Normalized errors

- `ProviderUnavailable` and `ProviderTimeout`: transient candidates.
- `ProviderRateLimited`: transient candidate with optional `retry_after`.
- `ProviderAuthenticationError` and `ProviderInvalidRequest`: non-retryable.
- `ProviderResponseError`: malformed or unexpected provider response.

The client does not automatically retry or silently fail over. Retry policy, circuit breakers, and fallback routing are separate concerns. Retryability metadata is guidance for an explicit policy, not permission to retry a non-idempotent operation.

## Deliberate scope

This contract covers text-only, non-streaming chat. Tool calling, JSON-schema output, image inputs, streaming, embeddings, and provider-specific reasoning controls are not flattened into fake common features. Capability negotiation is separate. Providers may differ in role support and parameter semantics; adapters must reject unsupported requests rather than silently changing meaning.

## Run locally

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

Tests require no network or model server. They are authored but have not been executed in the user's environment.
