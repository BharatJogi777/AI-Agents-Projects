"""Append-only workflow event journal with deterministic replay."""
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class Event:
    sequence: int
    name: str
    payload: dict[str, Any]

class ReplayError(ValueError):
    pass

class EventJournal:
    def __init__(self) -> None:
        self._events: list[Event] = []

    def append(self, name: str, payload: dict[str, Any]) -> Event:
        if not name.strip():
            raise ValueError("event name is required")
        event = Event(len(self._events) + 1, name, dict(payload))
        self._events.append(event)
        return event

    def events(self, after: int = 0) -> tuple[Event, ...]:
        if after < 0:
            raise ValueError("cursor cannot be negative")
        return tuple(e for e in self._events if e.sequence > after)

    def replay(self, initial: Any, reducer: Callable[[Any, Event], Any], *, until: int | None = None) -> Any:
        if until is not None and (until < 0 or until > len(self._events)):
            raise ReplayError("replay cursor is outside journal bounds")
        state = initial
        for event in self._events[:until]:
            state = reducer(state, event)
        return state

    def checkpoint(self, reducer: Callable[[Any, Event], Any], initial: Any = None) -> tuple[int, Any]:
        return len(self._events), self.replay(initial, reducer)
