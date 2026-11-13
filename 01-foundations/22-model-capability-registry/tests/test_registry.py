from datetime import datetime
from threading import Thread

import pytest

from model_registry import (
    CapabilityRequirement, CapabilityRegistry, DuplicateModelError,
    ModelCapabilities, ModelNotFoundError,
)


def model(model_id="local-small", **overrides):
    values = dict(
        model_id=model_id, providers=("ollama",), context_tokens=8192,
        max_output_tokens=2048, capabilities=frozenset({"chat", "streaming"}),
    )
    values.update(overrides)
    return ModelCapabilities(**values)


def test_select_requires_every_requested_feature_and_limit():
    registry = CapabilityRegistry((
        model("small"),
        model("tool-large", context_tokens=32768, capabilities=frozenset({"chat", "tools", "streaming"})),
        model("vision", providers=("cloud",), context_tokens=64000,
              capabilities=frozenset({"chat", "vision"}), input_modalities=frozenset({"text", "image"})),
    ))
    result = registry.select(CapabilityRequirement(
        provider="ollama", required_capabilities=frozenset({"tools"}), min_context_tokens=16000
    ))
    assert [entry.model_id for entry in result] == ["tool-large"]


def test_selection_is_deterministic():
    registry = CapabilityRegistry((model("z"), model("a"), model("large", context_tokens=32000)))
    assert [m.model_id for m in registry.select(CapabilityRequirement())] == ["large", "a", "z"]


def test_provider_specific_identifier_resolution():
    registry = CapabilityRegistry((model(
        "canonical", providers=("ollama", "proxy"),
        provider_model_ids={"ollama": "qwen3:4b", "proxy": "tenant/qwen"},
    ),))
    entry, concrete_id = registry.resolve("canonical", "ollama")
    assert entry.model_id == "canonical"
    assert concrete_id == "qwen3:4b"
    with pytest.raises(KeyError):
        registry.resolve("canonical", "missing")


def test_batch_registration_is_atomic_and_replace_is_explicit():
    registry = CapabilityRegistry((model("existing"),))
    with pytest.raises(DuplicateModelError):
        registry.register_many((model("new"), model("existing")))
    assert len(registry) == 1
    registry.register(model("existing", context_tokens=16000), replace=True)
    assert registry.get("existing").context_tokens == 16000


def test_validation_and_immutable_collections():
    with pytest.raises(ValueError):
        model("bad", capabilities=frozenset({"chat", "magic"}))
    entry = model("immutable", providers=("ollama", "proxy"),
                  provider_model_ids={"ollama": "qwen3:4b"})
    with pytest.raises(TypeError):
        entry.provider_model_ids["ollama"] = "changed"


def test_verified_timestamp_must_be_timezone_aware():
    with pytest.raises(ValueError):
        model("bad-time", verified_at=datetime(2026, 1, 1))


def test_unknown_model_has_domain_exception():
    with pytest.raises(ModelNotFoundError):
        CapabilityRegistry().get("absent")


def test_concurrent_registration_and_listing():
    registry, errors = CapabilityRegistry(), []
    def add(index):
        try:
            registry.register(model(f"m-{index}"))
        except Exception as exc:
            errors.append(exc)
    threads = [Thread(target=add, args=(i,)) for i in range(30)]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    assert not errors
    assert len(registry.list_models()) == 30
