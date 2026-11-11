"""Backward-compatible facade; use ollama_adapter for new code."""
from ollama_adapter import OllamaProvider,OllamaProviderError
__all__=["OllamaProvider","OllamaProviderError"]
