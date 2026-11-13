# AG-023 — Model Fallback Router

A bounded routing layer that selects capability-compatible model/provider pairs and moves to another route when a provider is unavailable or fails. This project is standalone and includes its own small capability registry.

## What it solves

A multi-provider application needs more than a list of API clients. It needs to decide which model is eligible for a request, prefer configured providers, handle failures without exposing provider internals, and stop after a finite number of attempts.

## Features

- Capability filtering: tool calling, JSON Schema, streaming, vision, context and output limits.
- Explicit provider preference ordering.
- Canonical model IDs mapped to provider-specific model IDs.
- Health checks that fail closed.
- Sequential fallback across unique model/provider routes.
- Bounded attempts at both router and request level.
- Typed provider errors that can disable fallback for request-wide failures.
- Injectable retry classifier and monotonic clock.
- Sanitized attempt records: provider, model, outcome, duration, exception type.
- No silent fallback after a provider explicitly marks an error non-fallbackable.
- No network dependency in the demo or tests.

## Project structure

- `registry.py`: immutable model capability records and thread-safe registry.
- `model_router/router.py`: request contract, provider protocol, route loop, result and attempt records.
- `model_router/errors.py`: routing/provider exceptions.
- `app.py`: public facade and runnable demo.
- `tests/test_router.py`: mocked provider and failure-path tests.

## Install and run

Python 3.12 or newer:

    python3.12 -m venv .venv
    source .venv/bin/activate
    pip install -e '.[dev]'
    pytest
    python app.py

The demo uses fake providers. It does not call Ollama or a cloud API.

## Basic usage

    from app import CapabilityRegistry, ModelCapabilities, ModelFallbackRouter

    class MyProvider:
        def chat(self, model_id: str, prompt: str) -> str:
            # Call the provider adapter here. Configure an HTTP timeout
            # inside that adapter; the router cannot cancel arbitrary sync I/O.
            return f"response from {model_id}"

    registry = CapabilityRegistry()
    registry.register(ModelCapabilities(
        model_id="local-chat",
        providers=("ollama",),
        context_tokens=8192,
        max_output_tokens=2048,
        provider_model_ids={"ollama": "qwen3:4b"},
    ))
    registry.register(ModelCapabilities(
        model_id="backup-chat",
        providers=("openai-compatible",),
        context_tokens=32768,
        max_output_tokens=4096,
        provider_model_ids={"openai-compatible": "tenant/chat-model"},
    ))

    router = ModelFallbackRouter(
        registry,
        providers={
            "ollama": MyProvider(),
            "openai-compatible": MyProvider(),
        },
        max_attempts=2,
    )
    result = router.generate(
        "Summarize the incident.",
        provider_order=("ollama", "openai-compatible"),
        min_context=4096,
        max_attempts=2,
    )
    print(result.provider, result.model_id, result.response)

## Failure policy

Unknown exceptions are considered fallback-eligible by default because adapters often surface provider-specific transport exceptions. Supply `retry_classifier` to tighten that policy:

    router = ModelFallbackRouter(
        registry,
        providers,
        retry_classifier=lambda exc: isinstance(exc, (TimeoutError, ConnectionError)),
    )

For a provider error that must stop the route chain (for example, a request-wide validation failure), raise:

    from model_router import ProviderCallError
    raise ProviderCallError("invalid request", fallback_allowed=False)

Provider-specific authentication failures may still be eligible for fallback to a different provider, depending on your policy. Do not blindly retry the same provider/model pair: this router visits each candidate pair at most once.

## Operational boundaries

- **Timeouts:** the provider adapter must enforce connect/read/write deadlines. A generic synchronous Python call cannot be safely cancelled by this router. Configure timeouts in the HTTPX client used by the provider adapters.
- **Retries:** this component performs route fallback, not repeated retries against one route. Combine it with a retry policy and circuit breaker at the provider-adapter boundary when appropriate.
- **Idempotency:** a chat completion is usually read-like, but providers may bill for failed/partial requests. If your operation triggers external side effects through tools, use idempotency keys and tool-level safeguards before enabling fallback.
- **Health checks:** health check exceptions are treated as unhealthy; this avoids sending traffic when readiness is unknown. Keep health checks cheap and cache their result rather than making a health request before every model call.
- **Capability data:** values must be verified against the exact provider deployment/model revision. This sample registry is in-memory and does not discover capabilities automatically.
- **Privacy:** attempt records intentionally store exception class names, not exception messages or prompts. Add carefully redacted tracing at the application boundary if needed.
- **Ranking:** provider preference is honored first, then larger context/output limits. This is a deterministic policy, not cost or latency optimization.
- **Budgets:** the router bounds the number of candidate calls. It does not bound tokens, monetary spend, or wall-clock duration; enforce those in the caller and provider adapters.

## Tests

Tests cover fallback after failure, provider preference, capability filtering, provider-specific IDs, health-check behavior, empty responses, attempt limits, non-fallbackable failures, retry classification, invalid requests, and no-compatible-route behavior. Tests are authored; run them locally with `pytest`.
