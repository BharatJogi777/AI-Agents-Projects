from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class AgentEvent:
    name: str
    step: int
    tool_name: str | None = None
    outcome: str = "ok"

class EventSink(Protocol):
    def emit(self, event: AgentEvent) -> None: ...

class LoggingEventSink:
    def emit(self, event: AgentEvent) -> None:
        import logging
        logging.getLogger("agent.events").info(
            "agent_event",
            extra={"event_name": event.name, "step": event.step,
                   "tool_name": event.tool_name, "outcome": event.outcome},
        )
