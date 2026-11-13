import pytest

from app.monitor import LatencyMonitor


def test_summary_aggregates_and_counts_slow_calls():
    monitor = LatencyMonitor(slow_threshold_ms=20)
    for value in (10, 20, 30, 40):
        monitor.observe("search", value)
    result = monitor.summary("search")
    assert result.count == 4
    assert result.minimum_ms == 10
    assert result.maximum_ms == 40
    assert result.mean_ms == 25
    assert result.slow_calls == 3


def test_measure_records_even_when_operation_raises():
    monitor = LatencyMonitor()
    with pytest.raises(RuntimeError):
        monitor.measure("failure", lambda: (_ for _ in ()).throw(RuntimeError()))
    assert monitor.summary("failure").count == 1


def test_empty_and_invalid_inputs():
    monitor = LatencyMonitor()
    with pytest.raises(KeyError):
        monitor.summary("missing")
    with pytest.raises(ValueError):
        monitor.observe("", 1)
    with pytest.raises(ValueError):
        LatencyMonitor(sample_limit=0)
