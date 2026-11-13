import pytest
from app.model_drift import compare_metrics

def test_threshold_comparison():
    result=compare_metrics({"accuracy":.95,"latency":100},{"accuracy":.90,"latency":105},thresholds={"accuracy":.02,"latency":10})
    assert result[0].drifted and not result[1].drifted

def test_mismatched_metrics_rejected():
    with pytest.raises(ValueError): compare_metrics({"a":1},{"b":1},thresholds={"a":1})

def test_negative_threshold_rejected():
    with pytest.raises(ValueError): compare_metrics({"a":1},{"a":2},thresholds={"a":-1})
