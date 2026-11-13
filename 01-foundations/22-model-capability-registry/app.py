"""Compatibility facade; prefer importing from model_registry directly."""
from model_registry import CapabilityRegistry, CapabilityRequirement, ModelCapabilities

__all__ = ["CapabilityRegistry", "CapabilityRequirement", "ModelCapabilities"]


def build_demo_registry() -> CapabilityRegistry:
    """Build an illustrative catalogue; values are not live provider claims."""
    registry = CapabilityRegistry()
    registry.register_many((
        ModelCapabilities(
            model_id="local-qwen", providers=("ollama",),
            provider_model_ids={"ollama": "qwen3:4b"},
            context_tokens=32768, max_output_tokens=8192,
            capabilities=frozenset({"chat", "tools", "json_mode", "streaming"}),
            source="Illustrative local configuration; verify against installed model/runtime",
        ),
        ModelCapabilities(
            model_id="cloud-example", providers=("openai-compatible",),
            context_tokens=128000, max_output_tokens=16384,
            capabilities=frozenset({"chat", "tools", "json_schema", "streaming", "vision"}),
            input_modalities=frozenset({"text", "image"}),
            source="Illustrative placeholder; replace with verified provider metadata",
        ),
    ))
    return registry


if __name__ == "__main__":
    selected = build_demo_registry().select(
        CapabilityRequirement(required_capabilities=frozenset({"tools"}), min_context_tokens=8192)
    )
    for model in selected:
        print(f"{model.model_id}: context={model.context_tokens}, providers={model.providers}")
