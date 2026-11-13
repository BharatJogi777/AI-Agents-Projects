"""Chronological incident event normalization and deduplication."""
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class Event:
    timestamp: str
    source: str
    message: str
    severity: str = "info"

def build_timeline(events: list[Event], *, max_events: int = 5000) -> list[dict]:
    if not 1 <= max_events <= 50000: raise ValueError("max_events must be between 1 and 50000")
    if len(events) > max_events: raise ValueError("event count exceeds max_events")
    normalized=[]; seen=set()
    for event in events:
        try: dt=datetime.fromisoformat(event.timestamp.replace("Z","+00:00"))
        except (ValueError,AttributeError) as exc: raise ValueError(f"invalid timestamp: {event.timestamp}") from exc
        if dt.tzinfo is None: raise ValueError("timestamps must include a timezone")
        if not event.source.strip() or not event.message.strip(): raise ValueError("source and message are required")
        key=(dt.astimezone(timezone.utc).isoformat(),event.source,event.message)
        if key in seen: continue
        seen.add(key)
        normalized.append({"timestamp":dt.astimezone(timezone.utc).isoformat(),"source":event.source,"severity":event.severity.lower(),"message":event.message})
    return sorted(normalized,key=lambda e:(e["timestamp"],e["source"],e["message"]))
