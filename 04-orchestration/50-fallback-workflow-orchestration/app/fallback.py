"""Execute ordered workflow alternatives until one succeeds."""
from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True)
class Attempt:
    strategy: str
    succeeded: bool
    value: Any = None
    error: str | None = None

@dataclass(frozen=True)
class FallbackResult:
    value: Any
    attempts: tuple[Attempt, ...]
    strategy: str

def execute_with_fallback(strategies: list[tuple[str, Callable[[], Any]]]) -> FallbackResult:
    if not strategies:
        raise ValueError("at least one strategy is required")
    names = [name for name, _ in strategies]
    if any(not name for name in names) or len(names) != len(set(names)):
        raise ValueError("strategy names must be non-empty and unique")
    attempts: list[Attempt] = []
    for name, action in strategies:
        try:
            value = action()
            attempts.append(Attempt(name, True, value=value))
            return FallbackResult(value, tuple(attempts), name)
        except Exception as exc:
            attempts.append(Attempt(name, False, error=f"{type(exc).__name__}: {exc}"))
    raise RuntimeError("all fallback strategies failed: " + "; ".join(a.strategy for a in attempts))
