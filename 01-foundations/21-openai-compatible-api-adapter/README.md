# AG-021 — OpenAI-compatible API adapter

A concrete synchronous adapter for non-streaming chat-completions APIs that implement the OpenAI-compatible `/chat/completions` contract. It maps application DTOs to HTTP JSON, adds optional bearer authentication, and validates provider responses before returning them.

## What this project teaches

- Keep provider-specific HTTP and JSON outside application/business logic.
- Reuse a pooled HTTPX client across requests.
- Treat API keys as secrets and never include response bodies in public exceptions.
- Normalize HTTP, timeout, and network failures into stable exception types.
- Bound response-body size and validate untrusted JSON.
- Make injected HTTP client ownership explicit.

## Architecture

```text
Application
   |
   v
Request / Message
   |
   v
OpenAICompatibleProvider
   |-- request mapping and optional Bearer auth
   |-- pooled HTTPX client
   |-- timeout / status / response-size handling
   |-- choice, content, finish-reason and usage validation
   v
OpenAI-compatible /chat/completions endpoint
```

- `openai_adapter/contracts.py`: validated request, message, and response DTOs.
- `openai_adapter/provider.py`: HTTP lifecycle, endpoint mapping, auth, error normalization, and response validation.
- `app.py`: backward-compatible import facade.

## Run

Requirements: Python 3.12+.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest
```

## Example

```python
import os
from app import Message, Request, OpenAICompatibleProvider

request = Request(
    model="your-model-name",
    messages=(
        Message("system", "You are a concise backend engineering tutor."),
        Message("user", "Explain connection pooling in two sentences."),
    ),
    temperature=0.2,
    max_tokens=120,
)

with OpenAICompatibleProvider(
    base_url=os.environ["LLM_BASE_URL"],  # e.g. https://api.example.com/v1
    api_key=os.environ.get("LLM_API_KEY"),
    timeout=90,
) as provider:
    response = provider.chat(request)

print(response.content)
print(response.usage)
```

Do not hardcode real API keys in source code, test fixtures, or committed configuration. Supply secrets through environment variables or a secret manager.

## Configuration and lifecycle

| Setting | Default | Notes |
|---|---:|---|
| `base_url` | Required | API root; include `/v1` if the server expects it |
| `api_key` | `None` | Optional bearer token; omitted when no key is configured |
| `timeout` | `60` seconds | HTTPX timeout |
| `max_response_bytes` | `8 MiB` | Response stream is stopped when this limit is exceeded |

Create one provider per application process and reuse it. Close it at application shutdown or use a `with` block. An injected `httpx.Client` remains caller-owned. For a FastAPI service, create the provider in application lifespan and close it during lifespan shutdown, not once per request.

## Error model

- `ProviderTimeout`: request timed out.
- `ProviderUnavailable`: connection/network failure or provider 5xx response.
- `ProviderRateLimited`: HTTP 429; numeric `Retry-After` is available as `retry_after`.
- `ProviderAuthenticationError`: HTTP 401/403.
- `ProviderInvalidRequest`: HTTP 400/404/405/413/422.
- `ProviderResponseError`: malformed JSON, invalid response shape/usage, or oversized response.
- `ProviderError`: common base class.

Public exception messages do not contain response bodies or transport details because those can contain secrets or user prompts. The original low-level exception remains available as `__cause__` for controlled diagnostics.

## Compatibility boundaries

“OpenAI-compatible” is not a guarantee that every vendor supports every option identically. This exercise deliberately implements only non-streaming text chat with `messages`, `temperature`, `max_tokens`, and optional bearer auth. It does not claim support for streaming, tool calls, JSON-schema response formats, images, provider-specific headers, or alternate token-limit fields such as `max_completion_tokens`. Add such features as explicit capabilities with dedicated tests rather than guessing based on vendor names.

The adapter reads the first choice only. It permits missing usage metadata because some compatible servers omit it. It expects assistant content to be a string; multimodal content arrays require a separate contract.

## Tests

Tests use HTTPX `MockTransport`, so they do not need a live endpoint or paid API key. Tests are authored but have not been executed in this repository environment.
