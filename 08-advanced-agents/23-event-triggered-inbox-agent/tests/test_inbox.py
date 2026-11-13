import pytest
from app.inbox import InboxEvent, triage_inbox

def test_classifies_and_flags_unknown_sender():
    rows = triage_inbox([InboxEvent("1","ops@example.com","URGENT outage","2026-01-01")], trusted_domains={"example.com"})
    assert rows[0].priority == "high"
    assert rows[0].requires_human_review

def test_promotion_is_low_priority():
    row = triage_inbox([InboxEvent("2","shop@example.com","Sale today","now")])[0]
    assert row.category == "promotion"

def test_rejects_duplicate_or_malformed_events():
    e = InboxEvent("x","bad","Hello","now")
    with pytest.raises(ValueError): triage_inbox([e])
    good = InboxEvent("x","a@b.com","Hello","now")
    with pytest.raises(ValueError): triage_inbox([good,good])
