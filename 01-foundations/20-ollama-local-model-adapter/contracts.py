"""Validated request and response DTOs for this standalone adapter exercise."""
from dataclasses import dataclass, field
from math import isfinite
from typing import Any

@dataclass(frozen=True, slots=True)
class ChatMessage:
    role: str
    content: str
    def __post_init__(self) -> None:
        if self.role not in {"system", "user", "assistant"}:
            raise ValueError("role must be system, user, or assistant")
        if not isinstance(self.content, str):
            raise TypeError("content must be text")

@dataclass(frozen=True, slots=True)
class ChatRequest:
    messages: tuple[ChatMessage, ...]
    model: str
    temperature: float = 0.0
    max_tokens: int = 512
    def __post_init__(self) -> None:
        if not isinstance(self.messages, tuple) or not self.messages:
            raise ValueError("messages must be a non-empty tuple")
        if any(not isinstance(message, ChatMessage) for message in self.messages):
            raise TypeError("messages must contain ChatMessage instances")
        if not isinstance(self.model, str) or not self.model.strip():
            raise ValueError("model is required")
        if isinstance(self.temperature, bool) or not isinstance(self.temperature, (int, float)):
            raise TypeError("temperature must be numeric")
        if not isfinite(self.temperature) or not 0 <= self.temperature <= 2:
            raise ValueError("temperature must be finite and between 0 and 2")
        if type(self.max_tokens) is not int or not 1 <= self.max_tokens <= 32768:
            raise ValueError("max_tokens must be an integer between 1 and 32768")

@dataclass(frozen=True, slots=True)
class ChatResponse:
    content: str
    model: str
    finish_reason: str | None = None
    usage: dict[str, int] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)