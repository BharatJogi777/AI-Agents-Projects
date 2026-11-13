"""Verify append-only audit events linked with SHA-256 hashes."""
from dataclasses import dataclass
import hashlib
import json

@dataclass(frozen=True)
class Event:
    sequence: int
    payload: dict
    previous_hash: str
    event_hash: str

def event_digest(sequence: int, payload: dict, previous_hash: str) -> str:
    body = json.dumps({"sequence": sequence, "payload": payload, "previous_hash": previous_hash}, sort_keys=True, separators=(",",":"), ensure_ascii=False)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()

def verify_chain(events: list[Event]) -> tuple[bool, int | None]:
    previous = "GENESIS"
    for expected_sequence, event in enumerate(events, start=1):
        if event.sequence != expected_sequence or event.previous_hash != previous:
            return False, expected_sequence
        if event.event_hash != event_digest(event.sequence, event.payload, event.previous_hash):
            return False, expected_sequence
        previous = event.event_hash
    return True, None

def append_event(events: list[Event], payload: dict) -> Event:
    if not isinstance(payload, dict):
        raise ValueError("payload must be a dictionary")
    valid, broken_at = verify_chain(events)
    if not valid:
        raise ValueError(f"cannot append to invalid chain at event {broken_at}")
    previous = events[-1].event_hash if events else "GENESIS"
    sequence = len(events) + 1
    return Event(sequence, payload, previous, event_digest(sequence, payload, previous))
