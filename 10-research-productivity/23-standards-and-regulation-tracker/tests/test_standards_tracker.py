import pytest
from app.standards_tracker import review_updates

def test_detects_version_and_status_change():
    result = review_updates(previous={"iso": {"version":"1", "status":"active"}}, current={"iso": {"version":"2", "status":"active"}})
    assert result[0].change == "changed"
    assert result[0].review_required is True

def test_new_record_requires_review():
    result = review_updates(previous={}, current={"law": {"version":"2026"}})
    assert result[0].change == "added"

def test_rejects_invalid_record():
    with pytest.raises(ValueError):
        review_updates(previous={"bad": "text"}, current={})
