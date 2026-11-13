"""Backward-compatible facade; use llm_adapter for new code."""
from llm_adapter import (
    ChatMessage, ChatRequest, ChatResponse, LLMClient, LLMProvider,
    ProviderAuthenticationError, ProviderContractError, ProviderError,
    ProviderInvalidRequest, ProviderNotRegistered, ProviderRateLimited,
    ProviderResponseError, ProviderTimeout, ProviderUnavailable,
)

__all__ = [
    "ChatMessage", "ChatRequest", "ChatResponse", "LLMClient", "LLMProvider",
    "ProviderContractError", "ProviderNotRegistered", "ProviderError",
    "ProviderUnavailable", "ProviderTimeout", "ProviderRateLimited",
    "ProviderAuthenticationError", "ProviderInvalidRequest", "ProviderResponseError",
]
