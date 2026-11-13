"""Provider-neutral, validated request and response contracts."""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

_ALLOWED_ROLES = frozenset({"system", "user", "assistant", "tool"})
_MAX_METADATA_BYTES = 64_000
_MAX_RAW_BYTES = 64_000


def _json_mapping(value: Mapping[str, Any], *, label: str, max_bytes: int) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{label} must be a mapping")
    try:
        encoded = json.dumps(dict(value), ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    except (TypeError, ValueError, RecursionError) as exc:
        raise ValueError(f"{label} must contain finite JSON-compatible values") from exc
    if len(encoded.encode("utf-8")) > max_bytes:
        raise ValueError(f"{label} exceeds {max_bytes} UTF-8 bytes")
    # A JSON round trip detaches nested mutable values and rejects custom objects.
    detached = json.loads(encoded)
    return MappingProxyType(detached)


@dataclass(frozen=True, slots=True)
class ChatMessage:
    role: str
    content: str

    def __post_init__(self) -> None:
        if not isinstance(self.role, str) or self.role not in _ALLOWED_ROLES:
            raise ValueError("role must be system, user, assistant, or tool")
        if not isinstance(self.content, str):
            raise TypeError("message content must be text")
        if len(self.content.encode("utf-8")) > 1_000_000:
            raise ValueError("message content exceeds 1 MB")


@dataclass(frozen=True, slots=True)
class ChatRequest:
    messages: tuple[ChatMessage, ...]
    model: str
    temperature: float = 0.0
    max_tokens: int = 512
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.messages, (tuple, list)) or not self.messages:
            raise ValueError("messages must be a non-empty tuple or list")
        messages = tuple(self.messages)
        if any(not isinstance(message, ChatMessage) for message in messages):
            raise TypeError("every message must be a ChatMessage")
        if sum(len(message.content.encode("utf-8")) for message in messages) > 4_000_000:
            raise ValueError("combined message content exceeds 4 MB")
        if not isinstance(self.model, str) or not self.model.strip() or len(self.model) > 200:
            raise ValueError("model is required and must be at most 200 characters")
        if isinstance(self.temperature, bool) or not isinstance(self.temperature, (int, float)):
            raise ValueError("temperature must be a finite number in [0, 2]")
        if not math.isfinite(self.temperature) or not 0 <= self.temperature <= 2:
            raise ValueError("temperature must be a finite number in [0, 2]")
        if type(self.max_tokens) is not int or not 1 <= self.max_tokens <= 32768:
            raise ValueError("max_tokens must be an integer in [1, 32768]")
        object.__setattr__(self, "messages", messages)
        object.__setattr__(self, "metadata", _json_mapping(
            self.metadata, label="metadata", max_bytes=_MAX_METADATA_BYTES
        ))


@dataclass(frozen=True, slots=True)
class ChatResponse:
    content: str
    model: str
    finish_reason: str | None = None
    usage: Mapping[str, int] = field(default_factory=dict)
    raw: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.content, str):
            raise TypeError("response content must be text")
        if not isinstance(self.model, str) or not self.model.strip() or len(self.model) > 200:
            raise ValueError("response model is required and must be at most 200 characters")
        if self.finish_reason is not None and not isinstance(self.finish_reason, str):
            raise TypeError("finish_reason must be text or None")
        if not isinstance(self.usage, Mapping):
            raise TypeError("usage must be a mapping")
        usage = dict(self.usage)
        if any(not isinstance(key, str) or type(value) is not int or value < 0
               for key, value in usage.items()):
            raise ValueError("usage must map strings to non-negative integers")
        object.__setattr__(self, "usage", MappingProxyType(usage))
        object.__setattr__(self, "raw", _json_mapping(
            self.raw, label="raw provider metadata", max_bytes=_MAX_RAW_BYTES
        ))
