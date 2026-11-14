import pytest
from app.thread_summary import summarize_thread

def test_orders_messages_and_extracts_questions():
    r=summarize_thread(messages=[{"sender":"B","timestamp":"2026-02-02","body":"Can you approve?"},{"sender":"A","timestamp":"2026-02-01","body":"Please review."}])
    assert r.participants==("A","B")
    assert r.chronological_messages[0].startswith("2026-02-01")
    assert r.open_questions==("Can you approve?",)

def test_rejects_empty_thread():
    with pytest.raises(ValueError): summarize_thread(messages=[])
