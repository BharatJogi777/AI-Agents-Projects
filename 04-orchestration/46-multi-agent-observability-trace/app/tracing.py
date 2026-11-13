"""Record correlated spans for multi-agent workflow execution."""
from dataclasses import dataclass, field
from time import monotonic
from typing import Any

@dataclass(frozen=True)
class Span:
    trace_id: str
    span_id: str
    parent_id: str | None
    name: str
    started_at: float
    ended_at: float
    attributes: dict[str, Any] = field(default_factory=dict)

    @property
    def duration(self) -> float:
        return max(0.0, self.ended_at - self.started_at)

class TraceRecorder:
    def __init__(self, clock=monotonic):
        self._clock = clock
        self._spans: list[Span] = []
        self._ids: set[str] = set()

    def record(self, trace_id: str, span_id: str, name: str, *,
               parent_id: str | None = None, started_at: float | None = None,
               ended_at: float | None = None, attributes: dict[str, Any] | None = None) -> Span:
        if not trace_id or not span_id or not name:
            raise ValueError("trace id, span id, and name are required")
        if span_id in self._ids:
            raise ValueError("span id must be unique")
        start = self._clock() if started_at is None else started_at
        end = self._clock() if ended_at is None else ended_at
        if end < start:
            raise ValueError("span end precedes start")
        if parent_id and parent_id not in self._ids:
            raise ValueError("parent span must be recorded before child")
        span = Span(trace_id, span_id, parent_id, name, start, end, dict(attributes or {}))
        self._spans.append(span); self._ids.add(span_id)
        return span

    def for_trace(self, trace_id: str) -> tuple[Span, ...]:
        return tuple(s for s in self._spans if s.trace_id == trace_id)

    def critical_path_duration(self, trace_id: str) -> float:
        spans = self.for_trace(trace_id)
        return max((s.duration for s in spans), default=0.0)
