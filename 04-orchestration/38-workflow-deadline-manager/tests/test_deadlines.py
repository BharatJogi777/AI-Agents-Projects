import pytest
from datetime import datetime, timedelta, timezone
from app.deadlines import DeadlineManager

def test_deadline_expiration_and_remaining():
    now=[datetime(2026,1,1,tzinfo=timezone.utc)]
    m=DeadlineManager(lambda: now[0]); m.schedule("wf",timedelta(seconds=10))
    assert m.remaining("wf") == timedelta(seconds=10)
    now[0] += timedelta(seconds=11)
    assert [d.workflow_id for d in m.expired()] == ["wf"]

def test_validation_and_cancel():
    m=DeadlineManager()
    with pytest.raises(ValueError): m.schedule("",timedelta(seconds=1))
    m.schedule("wf",timedelta(seconds=1))
    assert m.cancel("wf") and not m.cancel("wf")
