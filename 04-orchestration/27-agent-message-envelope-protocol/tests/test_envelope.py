import pytest
from app.envelope import MessageEnvelope, Inbox

def test_delivery_and_deduplication():
    m = MessageEnvelope.create("planner", "worker", "task", {"id": 1})
    inbox = Inbox("worker")
    assert inbox.deliver(m) is True
    assert inbox.deliver(m) is False
    assert len(inbox.receive("task")) == 1

def test_wrong_recipient_and_expiry():
    m = MessageEnvelope.create("a", "b", "task", {})
    with pytest.raises(ValueError): Inbox("c").deliver(m)
    expired = MessageEnvelope.create("a", "b", "task", {}, ttl_seconds=1)
    from datetime import timedelta
    with pytest.raises(ValueError): Inbox("b").deliver(expired, expired.expires_at + timedelta(seconds=1))

def test_invalid_creation():
    with pytest.raises(ValueError): MessageEnvelope.create("", "b", "task", {})
