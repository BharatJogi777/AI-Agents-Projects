"""Tokenizer abstractions used by the context-window planner."""
from typing import Protocol

class TokenCounter(Protocol):
    def count(self, text: str) -> int: ...

class TokenCountError(ValueError):
    pass

class HeuristicTokenCounter:
    def __init__(self, chars_per_token: int = 4) -> None:
        if not isinstance(chars_per_token, int) or isinstance(chars_per_token, bool) or chars_per_token < 1:
            raise ValueError("chars_per_token must be a positive integer")
        self.chars_per_token = chars_per_token

    def count(self, text: str) -> int:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        return (len(text) + self.chars_per_token - 1) // self.chars_per_token

class FixedTokenCounter:
    """Deterministic counter for tests; unknown strings are rejected."""
    def __init__(self, counts: dict[str, int]) -> None:
        self._counts = dict(counts)

    def count(self, text: str) -> int:
        try:
            value = self._counts[text]
        except KeyError as exc:
            raise TokenCountError(f"no fixed token count configured for {text!r}") from exc
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise TokenCountError("fixed token counts must be non-negative integers")
        return value

class TiktokenCounter:
    """Optional tokenizer adapter for models supported by tiktoken."""
    def __init__(self, *, model: str | None = None, encoding_name: str | None = None) -> None:
        if (model is None) == (encoding_name is None):
            raise ValueError("provide exactly one of model or encoding_name")
        try:
            import tiktoken
        except ImportError as exc:
            raise RuntimeError("install with: pip install -e '.[tokenizer]'") from exc
        try:
            self._encoding = tiktoken.encoding_for_model(model) if model is not None else tiktoken.get_encoding(encoding_name)
        except (KeyError, ValueError) as exc:
            raise TokenCountError("unknown model or encoding for tiktoken") from exc

    def count(self, text: str) -> int:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        return len(self._encoding.encode(text))
