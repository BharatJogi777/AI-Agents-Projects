class ToolCallRejected(ValueError):
    """Untrusted model tool call failed validation before execution."""


class ToolHandlerFailed(RuntimeError):
    """Trusted handler failed; the underlying exception is not model-facing."""
