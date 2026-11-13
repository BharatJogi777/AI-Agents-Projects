# AG-020 — Ollama local model adapter

A concrete synchronous adapter for Ollama's non-streaming POST /api/chat endpoint. It translates a small provider-neutral request DTO into Ollama's JSON payload and normalizes the response for application code.

## What this project teaches
- Keep provider-specific HTTP and JSON at the infrastructure boundary.
- Reuse one HTTPX client so TCP connections can be pooled.
- Set explicit timeouts and cap response-body size while streaming bytes.
- Normalize HTTP and transport failures into stable exception classes.
- Validate provider responses before exposing them to application code.
- Make HTTP client ownership explicit when injecting dependencies.

## Architecture

~~~text
Application -> ChatRequest / ChatMessage -> OllamaProvider
                                      |-> request mapping
                                      |-> pooled HTTPX client
                                      |-> timeout / status / body-size handling
                                      |-> response validation and usage mapping
                                      v
                                Ollama /api/chat
~~~

- contracts.py: validated request and response DTOs. Their shape mirrors AG-019 while keeping this exercise standalone.
- ollama_adapter/provider.py: HTTP lifecycle, status mapping, health/model listing, and chat.
- app.py: compatibility import facade.

## Run locally

Requirements: Python 3.12+ and Ollama installed and running.

~~~bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
ollama pull qwen3:4b
pytest
~~~

## Example

~~~python
from app import OllamaProvider
from contracts import ChatMessage, ChatRequest

request = ChatRequest(
    messages=(
        ChatMessage('system', 'You are a concise backend engineering tutor.'),
        ChatMessage('user', 'Explain connection pooling in two sentences.'),
    ),
    model='qwen3:4b',
    temperature=0.2,
    max_tokens=120,
)

with OllamaProvider(base_url='http://localhost:11434', timeout_seconds=90) as ollama:
    response = ollama.chat(request)

print(response.content)
print(response.usage)
~~~

## Configuration and lifecycle

| Setting | Default | Notes |
|---|---:|---|
| base_url | http://localhost:11434 | HTTP(S) server root; credentials, query, fragment, and path are rejected |
| timeout_seconds | 60 | Applied through HTTPX timeout configuration |
| max_response_bytes | 8 MiB | The response stream is stopped when this limit is exceeded |

Create one provider per application process and reuse it. Use a with block or call close() during application shutdown. If an httpx.Client is injected, it remains caller-owned and must be closed by the caller. Do not create a new provider for every prompt.

For containerized APIs, localhost refers to the API container itself. Configure the Ollama service hostname on the Docker network or the appropriate host gateway.

## Error model

- OllamaTimeout: request timed out.
- OllamaUnavailable: connection/network failure or Ollama 5xx response.
- OllamaRateLimited: HTTP 429; retry_after is populated for a numeric Retry-After header.
- OllamaAuthenticationError: HTTP 401/403.
- OllamaInvalidRequest: HTTP 400/404/405/413/422 (a missing model commonly appears as 404).
- OllamaResponseError: malformed JSON, invalid response shape, invalid usage counters, or oversized response.
- OllamaProviderError: common base class.

Exception messages intentionally omit response bodies and transport details because they may contain prompts or secrets. The original low-level exception remains available as __cause__ for controlled internal diagnostics.

## Scope and non-goals

This adapter implements non-streaming text chat, a basic health check (GET /api/tags), and installed-model listing. It does not claim support for streaming, tool calls, JSON-schema output, image input, embeddings, or model lifecycle management. Add those as explicit capabilities with separate contracts and tests rather than silently overloading this API.

Tests use HTTPX MockTransport, so they do not require a running Ollama server or a downloaded model. Tests are authored but have not been executed in this repository environment.