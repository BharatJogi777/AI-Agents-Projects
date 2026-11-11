class AgentError(RuntimeError):
    """Base class for expected agent failures."""
class ModelProtocolError(AgentError):
    """Provider response violated the normalized chat contract."""
class ToolExecutionError(AgentError):
    """A registered tool failed or received invalid input."""
