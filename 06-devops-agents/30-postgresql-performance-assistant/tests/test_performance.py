from app.performance import analyze_snapshot
import pytest

def test_prioritizes_deadlocks():
    result=analyze_snapshot({"deadlocks":2,"cache_hit_ratio":0.7})
    assert result[0].priority=="critical"

def test_rejects_invalid_cache_ratio():
    with pytest.raises(ValueError): analyze_snapshot({"cache_hit_ratio":-0.1})
