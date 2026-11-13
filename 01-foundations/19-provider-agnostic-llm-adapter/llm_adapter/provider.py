"""Provider protocol and explicit registry-backed client."""
from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Protocol

from .contracts import ChatRequest, ChatResponse


class LLMProvider(Protocol):
    """Implemented by Ollama, OpenAI-compatible, or other provider adapters."""
    def chat(self, request: ChatRequest) -> ChatResponse:
        ...


class ProviderNotRegistered(LookupError):
    """Raised when a requested provider alias is not configured."""


class ProviderContractError(TypeError):
    """Raised when an adapter violates the normalized response contract."""


class LLMClient:
    """Routes requests to an explicitly configured provider.

    Provider failures pass through unchanged. Adapters translate vendor errors
    into llm_adapter.errors types; this client never guesses retryability.
    """
    def __init__(self, providers: Mapping[str, LLMProvider], default_provider: str) -> None:
        if not isinstance(providers, Mapping) or not providers:
            raise ValueError("at least one provider must be registered")
        if not isinstance(default_provider, str) or not default_provider.strip():
            raise ValueError("default_provider must be a non-empty string")
        copied = dict(providers)
        if any(not isinstance(name, str) or not name.strip() for name in copied):
            raise ValueError("provider names must be non-empty strings")
        if any(not callable(getattr(provider, "chat", None)) for provider in copied.values()):
            raise TypeError("every provider must implement callable chat(request)")
        if default_provider not in copied:
            raise ValueError("default provider must be registered")
        self._providers = MappingProxyType(copied)
        self.default_provider = default_provider

    @property
    def provider_names(self) -> tuple[str, ...]:
        return tuple(self._providers)

    def chat(self, request: ChatRequest, provider: str | None = None) -> ChatResponse:
        if not isinstance(request, ChatRequest):
            raise TypeError("request must be a ChatRequest")
        selected = self.default_provider if provider is None else provider
        if not isinstance(selected, str) or not selected.strip():
            raise ValueError("provider must be a non-empty string")
        adapter = self._providers.get(selected)
        if adapter is None:
            raise ProviderNotRegistered(f"provider is not registered: {selected}")
        response = adapter.chat(request)
        if not isinstance(response, ChatResponse):
            raise ProviderContractError("provider adapter must return ChatResponse")
        return response
