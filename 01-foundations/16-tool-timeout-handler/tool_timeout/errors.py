class ToolTimedOut(TimeoutError):
    """The tool's own configured execution deadline elapsed."""


class RequestDeadlineExceeded(TimeoutError):
    """The caller's overall request deadline elapsed during tool execution."""
