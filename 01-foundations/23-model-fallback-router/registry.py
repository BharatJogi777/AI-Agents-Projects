"""Standalone capability catalogue used by the fallback router."""
from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from threading import RLock
from typing import Mapping


@dataclass(frozen=True, slots=True)
class ModelCapabilities:
    model_id: str
    providers: tuple[str, ...]
    context_tokens: int
    max_output_tokens: int
    supports_tools: bool = False
    supports_json_schema: bool = False
    supports_streaming: bool = False
    supports_vision: bool = False
    provider_model_ids: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.model_id, str) or not self.model_id.strip():
            raise ValueError("model_id is required")
        if not isinstance(self.providers, tuple) or not self.providers:
            raise ValueError("providers must be a non-empty tuple")
        if any(not isinstance(p, str) or not p.strip() for p in self.providers):
            raise ValueError("provider names must be non-empty strings")
        if len(set(self.providers)) != len(self.providers):
            raise ValueError("providers must be unique")
        for name, value in (("context_tokens", self.context_tokens),
                            ("max_output_tokens", self.max_output_tokens)):
            if type(value) is not int or value < 1:
                raise ValueError(f"{name} must be a positive integer")
        if self.max_output_tokens > self.context_tokens:
            raise ValueError("max_output_tokens cannot exceed context_tokens")
        for name in ("supports_tools", "supports_json_schema", "supports_streaming", "supports_vision"):
            if type(getattr(self, name)) is not bool:
                raise TypeError(f"{name} must be boolean")
        if not isinstance(self.provider_model_ids, Mapping):
            raise TypeError("provider_model_ids must be a mapping")
        mapped = {}
        for provider, model_id in self.provider_model_ids.items():
            if provider not in self.providers:
                raise ValueError("provider_model_ids keys must exist in providers")
            if not isinstance(model_id, str) or not model_id.strip():
                raise ValueError("provider model IDs must be non-empty strings")
            mapped[provider] = model_id
        object.__setattr__(self, "provider_model_ids", MappingProxyType(mapped))

    def provider_model_id(self, provider: str) -> str:
        if provider not in self.providers:
            raise KeyError(f"{provider!r} is not configured for {self.model_id!r}")
        return self.provider_model_ids.get(provider, self.model_id)


class CapabilityRegistry:
    """Thread-safe, duplicate-safe in-memory model catalogue."""

    def __init__(self) -> None:
        self._models: dict[str, ModelCapabilities] = {}
        self._lock = RLock()

    def register(self, item: ModelCapabilities, *, replace: bool = False) -> None:
        if not isinstance(item, ModelCapabilities):
            raise TypeError("item must be ModelCapabilities")
        with self._lock:
            if item.model_id in self._models and not replace:
                raise ValueError(f"duplicate model: {item.model_id}")
            self._models[item.model_id] = item

    def get(self, model_id: str) -> ModelCapabilities:
        with self._lock:
            try:
                return self._models[model_id]
            except KeyError as exc:
                raise KeyError(f"unknown model: {model_id}") from exc

    def list_models(self) -> tuple[ModelCapabilities, ...]:
        with self._lock:
            return tuple(self._models[key] for key in sorted(self._models))

    def select(self, *, tools: bool = False, json_schema: bool = False,
               streaming: bool = False, vision: bool = False,
               min_context: int = 1, min_output: int = 1) -> list[ModelCapabilities]:
        for name, value in (("tools", tools), ("json_schema", json_schema),
                            ("streaming", streaming), ("vision", vision)):
            if type(value) is not bool:
                raise TypeError(f"{name} must be boolean")
        for name, value in (("min_context", min_context), ("min_output", min_output)):
            if type(value) is not int or value < 1:
                raise ValueError(f"{name} must be a positive integer")
        with self._lock:
            models = tuple(self._models.values())
        return [
            model for model in models
            if model.context_tokens >= min_context
            and model.max_output_tokens >= min_output
            and (not tools or model.supports_tools)
            and (not json_schema or model.supports_json_schema)
            and (not streaming or model.supports_streaming)
            and (not vision or model.supports_vision)
        ]
