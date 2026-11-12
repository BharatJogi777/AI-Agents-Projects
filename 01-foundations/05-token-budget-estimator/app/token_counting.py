"""Token-counting abstractions and explicit model-specific adapters."""
from math import ceil
from typing import Protocol


class TokenCounter(Protocol):
    """A counter compatible with the target model's tokenizer."""
    def count(self, text: str) -> int: ...


class TokenCountError(ValueError):
    """Raised when a tokenizer returns an invalid token count."""


class HeuristicTokenCounter:
    """Character-based approximation; never treat this as an exact tokenizer."""
    def __init__(self, chars_per_token: float = 4.0) -> None:
        if chars_per_token <= 0:
            raise ValueError("chars_per_token must be greater than zero")
        self._chars_per_token = chars_per_token

    def count(self, text: str) -> int:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        if not text:
            return 0
        return max(1, ceil(len(text) / self._chars_per_token))


class FixedTokenCounter:
    """Deterministic counter for unit tests and reproducible examples."""
    def __init__(self, counts: dict[str, int]) -> None:
        if any(not isinstance(value, int) or isinstance(value, bool) or value < 0
               for value in counts.values()):
            raise ValueError("token counts must be non-negative integers")
        self._counts = dict(counts)

    def count(self, text: str) -> int:
        try:
            return self._counts[text]
        except KeyError as exc:
            raise ValueError("no fixed token count configured for text") from exc


class TiktokenCounter:
    """Exact tokenizer adapter for supported OpenAI model encodings.

    Install the optional extra: pip install -e '.[tiktoken]'.
    Token counts still may not include provider-side message/tool framing.
    """
    def __init__(self, *, model: str | None = None, encoding_name: str | None = None) -> None:
        if bool(model) == bool(encoding_name):
            raise ValueError("provide exactly one of model or encoding_name")
        try:
            import tiktoken
        except ImportError as exc:
            raise RuntimeError(
                "tiktoken is optional; install it with: pip install -e '.[tiktoken]'"
            ) from exc
        try:
            self._encoding = (
                tiktoken.encoding_for_model(model)
                if model is not None
                else tiktoken.get_encoding(encoding_name)
            )
        except KeyError as exc:
            raise ValueError("unknown model or tokenizer encoding") from exc

    def count(self, text: str) -> int:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        return len(self._encoding.encode(text))
