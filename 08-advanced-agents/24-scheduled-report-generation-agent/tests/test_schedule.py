import pytest
from datetime import datetime, timezone, timedelta
from app.schedule import ReportSchedule, due_reports

def test_returns_due_schedule_with_stable_key():
    now = datetime(2026,1,1,12,tzinfo=timezone.utc)
    last = now - timedelta(hours=1)
    result = due_reports([ReportSchedule("daily",60)], now=now, last_run={"daily":last})
    assert result[0].scheduled_for == now.isoformat()
    assert result[0].idempotency_key.startswith("daily:")

def test_skips_disabled_and_not_yet_due():
    now = datetime(2026,1,1,tzinfo=timezone.utc)
    rows = due_reports([ReportSchedule("off",5,False),ReportSchedule("later",60)], now=now, last_run={"later":now})
    assert rows == ()

def test_requires_aware_time_and_valid_interval():
    with pytest.raises(ValueError): due_reports([], now=datetime(2026,1,1))
    with pytest.raises(ValueError): due_reports([ReportSchedule("x",0)], now=datetime.now(timezone.utc))
