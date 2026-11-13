from app.latency import investigate_redis
import pytest

def test_detects_high_latency_and_evictions():
    out=investigate_redis({"p95_latency_ms":20,"p99_latency_ms":30,"evictions":4})
    assert any(x.signal=="Key evictions" for x in out)

def test_rejects_invalid_percentile_order():
    with pytest.raises(ValueError): investigate_redis({"p95_latency_ms":20,"p99_latency_ms":10})
