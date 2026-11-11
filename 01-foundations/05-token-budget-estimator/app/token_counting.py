"""Token-counting abstractions and an explicitly approximate fallback."""

from math import ceil
from typing import Protocol


class TokenCounter(Protocol):
    """A counter compatible with the target model's tokenizer."""

    def count(self, text: str) -> int:
        """Return the token count for text."""


class HeuristicTokenCounter:
    """Estimate tokens from character length; never treat this as exact."""

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
    """Useful in tests and examples where exact counts are supplied."""

    def __init__(self, counts: dict[str, int]) -> None:
        if any(value < 0 for value in counts.values()):
            raise ValueError("token counts cannot be negative")
        self._counts = dict(counts)

    def count(self, text: str) -> int:
        try:
            return self._counts[text]
        except KeyError as exc:
            raise ValueError("no fixed token count configured for text") from exc
