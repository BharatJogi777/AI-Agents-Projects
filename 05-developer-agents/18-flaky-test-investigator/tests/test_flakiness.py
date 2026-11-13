import pytest
from app.flakiness import analyze_runs, to_json


def test_detects_mixed_outcomes_and_duration_variation():
    data = [{"test_id": "t", "outcome": "passed", "duration": 0.1},
            {"test_id": "t", "outcome": "failed", "duration": 0.9}]
    result = analyze_runs(data)[0]
    assert result.suspected_flaky
    assert result.failure_rate == 0.5
    assert result.duration_stddev > 0
    assert '"test_id"' in to_json([result])


def test_stable_passes_not_flagged():
    result = analyze_runs([{"test_id": "t", "outcome": "passed", "duration": 1}])[0]
    assert not result.suspected_flaky


def test_rejects_invalid_records():
    with pytest.raises(ValueError):
        analyze_runs([{"test_id": "t", "outcome": "unknown", "duration": 1}])
