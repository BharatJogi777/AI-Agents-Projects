import pytest
from app.incident_timeline import Event, build_timeline

def test_sorts_and_deduplicates_events():
    events=[Event("2026-01-01T00:02:00Z","api","degraded"),Event("2026-01-01T00:01:00+00:00","db","slow"),Event("2026-01-01T00:02:00Z","api","degraded")]
    result=build_timeline(events)
    assert [e["source"] for e in result] == ["db","api"]

def test_rejects_naive_timestamp_and_invalid_limit():
    with pytest.raises(ValueError): build_timeline([Event("2026-01-01T00:00:00","api","x")])
    with pytest.raises(ValueError): build_timeline([],max_events=0)
