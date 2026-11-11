class ToolRegistrationError(ValueError):
    """Raised when a trusted tool definition is invalid."""


class ToolExecutionError(RuntimeError):
    """Safe public error for rejected or failed tool invocation."""
