import pytest
from app.audit_integrity import Event, append_event, verify_chain

def test_append_and_verify_chain():
    events = []
    events.append(append_event(events, {"action":"read"}))
    events.append(append_event(events, {"action":"search"}))
    assert verify_chain(events) == (True, None)

def test_detects_payload_tampering():
    event = append_event([], {"action":"read"})
    changed = Event(event.sequence, {"action":"delete"}, event.previous_hash, event.event_hash)
    assert verify_chain([changed]) == (False, 1)

def test_refuses_append_to_broken_chain():
    event = append_event([], {"action":"read"})
    changed = Event(event.sequence, {"action":"delete"}, event.previous_hash, event.event_hash)
    with pytest.raises(ValueError):
        append_event([changed], {"action":"write"})
