"""Backward-compatible facade; use openai_adapter for new code."""
from openai_adapter import Message,Request,Response,OpenAICompatibleProvider,ProviderError
__all__=["Message","Request","Response","OpenAICompatibleProvider","ProviderError"]
