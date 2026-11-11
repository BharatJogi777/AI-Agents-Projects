"""Backward-compatible facade; use circuit_breaker for new code."""
from circuit_breaker import CircuitBreaker,CircuitOpen,CircuitSnapshot,CircuitState
__all__=["CircuitBreaker","CircuitOpen","CircuitSnapshot","CircuitState"]
