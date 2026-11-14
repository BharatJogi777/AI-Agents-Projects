import pytest
from app.reading_list import curate_reading_list

def test_sorts_active_and_high_priority_items():
    result=curate_reading_list(items=[{"id":"b","title":"Later","status":"unread","priority":2,"due_date":"2026-12-01"},{"id":"a","title":"Now","status":"reading","priority":3,"due_date":"2026-11-20"}])
    assert result[0].item_id=="a"

def test_rejects_invalid_status():
    with pytest.raises(ValueError):
        curate_reading_list(items=[{"id":"x","title":"X","status":"unknown","priority":1,"due_date":"2026-01-01"}])
