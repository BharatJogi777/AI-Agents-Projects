"""Deterministic incident handoff summary from structured updates."""
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Update:
    timestamp: str
    author: str
    message: str
    status: str = "update"
    owner: str | None = None

def summarize_handoff(updates: list[Update]) -> dict:
    normalized=[]
    for u in updates:
        if not u.author.strip() or not u.message.strip(): raise ValueError("author and message are required")
        try: dt=datetime.fromisoformat(u.timestamp.replace("Z","+00:00"))
        except ValueError as exc: raise ValueError(f"invalid timestamp: {u.timestamp}") from exc
        if dt.tzinfo is None: raise ValueError("timestamps must include timezone")
        normalized.append((dt,u))
    normalized.sort(key=lambda pair:pair[0])
    open_items=[{"message":u.message,"owner":u.owner,"timestamp":u.timestamp} for _,u in normalized if u.status.lower() in {"open","blocked","action"}]
    return {"timeline":[{"timestamp":u.timestamp,"author":u.author,"status":u.status,"message":u.message} for _,u in normalized],"open_actions":open_items,"latest_update":normalized[-1][1].timestamp if normalized else None,"handoff_warning":"Confirm current status and owners with the outgoing responder."}
