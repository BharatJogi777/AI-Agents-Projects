"""Sanitized routing and provider error contracts."""

class ModelRoutingError(RuntimeError):
    """Base class for routing failures."""

class ProviderCallError(Exception):
    """Provider error with an explicit fallback policy."""
    def __init__(self, message: str, *, fallback_allowed: bool = True) -> None:
        super().__init__(message)
        self.fallback_allowed = fallback_allowed

class NoModelAvailable(ModelRoutingError):
    """No compatible route completed successfully."""
    def __init__(self, message: str, *, attempts: tuple[str, ...] = ()) -> None:
        super().__init__(message)
        self.attempts = attempts

class FallbackBudgetExceeded(NoModelAvailable):
    """The configured maximum provider attempts was reached."""
