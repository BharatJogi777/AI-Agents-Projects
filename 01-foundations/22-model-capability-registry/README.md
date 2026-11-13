# AG-022 — Model Capability Registry

A provider-independent, thread-safe catalogue of model metadata. Callers select a model by declared capabilities and limits, never by guessing from a model name.

## Why this exists

A model name does not reliably tell an application whether a particular deployment supports tool calling, JSON Schema, vision, audio, or a particular context window. Those facts can differ by provider, deployment, model revision, and runtime configuration. Keep them as explicit metadata and record where and when they were verified.

## Features

- Immutable, validated capability records.
- Canonical model IDs separated from provider-specific model IDs.
- Capability, modality, provider, context-window, and output-limit filtering.
- Deterministic result ordering.
- Thread-safe reads/writes and atomic batch registration.
- Explicit replacement semantics; duplicate IDs are rejected by default.
- Domain-specific errors and no implicit provider fallback.

## Quick start

    python3.12 -m venv .venv
    source .venv/bin/activate
    pip install -e '.[dev]'
    pytest
    python app.py

## Example

    from model_registry import CapabilityRegistry, CapabilityRequirement, ModelCapabilities

    registry = CapabilityRegistry()
    registry.register(ModelCapabilities(
        model_id="local-qwen",
        providers=("ollama",),
        provider_model_ids={"ollama": "qwen3:4b"},
        context_tokens=32768,
        max_output_tokens=8192,
        capabilities=frozenset({"chat", "tools", "json_mode", "streaming"}),
        input_modalities=frozenset({"text"}),
        output_modalities=frozenset({"text"}),
        source="Internal runtime probe",
    ))

    matches = registry.select(CapabilityRequirement(
        provider="ollama",
        required_capabilities=frozenset({"chat", "tools"}),
        min_context_tokens=16000,
        min_output_tokens=2048,
    ))
    for model in matches:
        canonical, provider_model = registry.resolve(model.model_id, "ollama")
        print(canonical.model_id, provider_model)

## Capability vocabulary

Capabilities: chat, tools, json_mode, json_schema, streaming, vision, audio_input, audio_output, embeddings.

Input/output modalities: text, image, audio, video. Feature flags must come from trusted provider documentation or a runtime probe; this package intentionally does not infer them.

## Design notes and limits

- This is an in-memory registry. Persist the source manifest in your configuration/database and rebuild the registry at startup.
- verified_at must be timezone-aware. source should identify the documentation, probe, or internal manifest used.
- A capability record is immutable after registration. Use replace=True to intentionally replace a record after re-verification.
- Selection ranks by descending context window, then output limit, then canonical ID. It does not claim that the first result is cheapest or fastest; add measured cost/latency signals before introducing those ranking policies.
- Context window is a total model context limit, not an estimate of remaining prompt budget. The caller must subtract prompt, tool, and reserved output tokens.
- Provider feature support can vary by API version and deployment. Keep records scoped to the actual deployment and refresh them when configuration changes.

## Tests

The suite covers validation, immutable metadata, feature intersection, provider-specific identifiers, atomic registration, deterministic ordering, domain errors, and concurrent registration. Tests are authored; run them locally with pytest.
