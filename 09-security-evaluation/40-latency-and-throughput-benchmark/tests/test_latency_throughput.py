import pytest
from app.latency_throughput import summarize_benchmark
def test_percentiles_and_throughput():
 r=summarize_benchmark([10,20,30,40,50],duration_seconds=2,completed_requests=20)
 assert r.p50_ms==30 and r.p95_ms==48 and r.p99_ms==pytest.approx(49.6) and r.throughput_rps==10
def test_invalid_samples_and_duration():
 with pytest.raises(ValueError): summarize_benchmark([],duration_seconds=1)
 with pytest.raises(ValueError): summarize_benchmark([1,-1],duration_seconds=1)
 with pytest.raises(ValueError): summarize_benchmark([1],duration_seconds=0)
