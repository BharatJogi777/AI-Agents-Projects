"""Validated, immutable model capability contracts.

Capability values are facts supplied by a provider manifest or a verified probe.
This module deliberately does not infer features from model names.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Mapping
import re

SUPPORTED_CAPABILITIES = frozenset({
    "chat", "tools", "json_mode", "json_schema", "streaming",
    "vision", "audio_input", "audio_output", "embeddings",
})
SUPPORTED_MODALITIES = frozenset({"text", "image", "audio", "video"})
_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/+-]{0,199}$")


def _identifier(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise ValueError(f"{field_name} must be a non-empty identifier (max 200 characters)")
    return value


@dataclass(frozen=True, slots=True)
class ModelCapabilities:
    """Canonical model identity and explicitly verified provider capabilities."""

    model_id: str
    providers: tuple[str, ...]
    context_tokens: int
    max_output_tokens: int
    capabilities: frozenset[str] = field(default_factory=lambda: frozenset({"chat"}))
    input_modalities: frozenset[str] = field(default_factory=lambda: frozenset({"text"}))
    output_modalities: frozenset[str] = field(default_factory=lambda: frozenset({"text"}))
    provider_model_ids: Mapping[str, str] = field(default_factory=dict)
    verified_at: datetime | None = None
    source: str | None = None

    def __post_init__(self) -> None:
        _identifier(self.model_id, "model_id")
        if not isinstance(self.providers, tuple) or not self.providers:
            raise ValueError("providers must be a non-empty tuple")
        providers = tuple(_identifier(p, "provider") for p in self.providers)
        if len(set(providers)) != len(providers):
            raise ValueError("providers must be unique")
        object.__setattr__(self, "providers", providers)

        for name, value in (("context_tokens", self.context_tokens),
                            ("max_output_tokens", self.max_output_tokens)):
            if type(value) is not int or value < 1:
                raise ValueError(f"{name} must be a positive integer")
        if self.max_output_tokens > self.context_tokens:
            raise ValueError("max_output_tokens cannot exceed context_tokens")

        for name, values, allowed in (
            ("capabilities", self.capabilities, SUPPORTED_CAPABILITIES),
            ("input_modalities", self.input_modalities, SUPPORTED_MODALITIES),
            ("output_modalities", self.output_modalities, SUPPORTED_MODALITIES),
        ):
            if not isinstance(values, (set, frozenset, tuple, list)):
                raise TypeError(f"{name} must be a collection of strings")
            normalized = frozenset(values)
            if any(not isinstance(v, str) or v not in allowed for v in normalized):
                raise ValueError(f"{name} contains unsupported values")
            object.__setattr__(self, name, normalized)

        if "chat" not in self.capabilities and "embeddings" not in self.capabilities:
            raise ValueError("a model must declare chat or embeddings capability")
        if not isinstance(self.provider_model_ids, Mapping):
            raise TypeError("provider_model_ids must be a mapping")
        mapped = {}
        for provider, provider_id in self.provider_model_ids.items():
            provider = _identifier(provider, "provider_model_ids key")
            mapped[provider] = _identifier(provider_id, "provider model ID")
            if provider not in providers:
                raise ValueError("provider_model_ids keys must exist in providers")
        object.__setattr__(self, "provider_model_ids", MappingProxyType(mapped))

        if self.verified_at is not None:
            if not isinstance(self.verified_at, datetime) or self.verified_at.tzinfo is None:
                raise ValueError("verified_at must be a timezone-aware datetime")
        if self.source is not None and (not isinstance(self.source, str) or not self.source.strip()):
            raise ValueError("source must be a non-empty string when supplied")

    def provider_model_id(self, provider: str) -> str:
        """Return provider-specific ID, or canonical ID when no override exists."""
        if provider not in self.providers:
            raise KeyError(f"{self.model_id!r} is not registered for provider {provider!r}")
        return self.provider_model_ids.get(provider, self.model_id)


@dataclass(frozen=True, slots=True)
class CapabilityRequirement:
    """A declarative query; every requested feature must be present."""

    provider: str | None = None
    required_capabilities: frozenset[str] = field(default_factory=frozenset)
    required_input_modalities: frozenset[str] = field(default_factory=lambda: frozenset({"text"}))
    required_output_modalities: frozenset[str] = field(default_factory=lambda: frozenset({"text"}))
    min_context_tokens: int = 1
    min_output_tokens: int = 1

    def __post_init__(self) -> None:
        for name, values, allowed in (
            ("required_capabilities", self.required_capabilities, SUPPORTED_CAPABILITIES),
            ("required_input_modalities", self.required_input_modalities, SUPPORTED_MODALITIES),
            ("required_output_modalities", self.required_output_modalities, SUPPORTED_MODALITIES),
        ):
            if not isinstance(values, (set, frozenset, tuple, list)):
                raise TypeError(f"{name} must be a collection")
            normalized = frozenset(values)
            if any(not isinstance(v, str) or v not in allowed for v in normalized):
                raise ValueError(f"{name} contains unsupported values")
            object.__setattr__(self, name, normalized)
        if self.provider is not None:
            _identifier(self.provider, "provider")
        for name, value in (("min_context_tokens", self.min_context_tokens),
                            ("min_output_tokens", self.min_output_tokens)):
            if type(value) is not int or value < 1:
                raise ValueError(f"{name} must be a positive integer")
