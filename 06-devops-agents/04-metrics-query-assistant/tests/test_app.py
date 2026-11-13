import pytest
from app.metrics_query import build_query

def test_builds_allowlisted_rate_query():
    assert build_query("http_requests_total",operation="rate") == "sum(rate(http_requests_total[5m]))"

def test_rejects_untrusted_metric_and_bad_window():
    with pytest.raises(ValueError): build_query("process_cpu_seconds_total")
    with pytest.raises(ValueError): build_query("up",window="5m] or vector(1)")

def test_histogram_quantile():
    assert "histogram_quantile" in build_query("http_request_duration_seconds_bucket",operation="p95")
