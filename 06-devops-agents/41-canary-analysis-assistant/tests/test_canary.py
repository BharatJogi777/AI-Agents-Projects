from app.canary import analyze_canary
import pytest

def test_detects_regression():
    result=analyze_canary({"errors":{"value":.01,"samples":1000}},{"errors":{"value":.03,"samples":1000}},tolerances={"errors":10})
    assert result.decision=="investigate_regression"

def test_rejects_mismatched_metrics():
    with pytest.raises(ValueError): analyze_canary({"a":{"value":1,"samples":10}},{"b":{"value":1,"samples":10}})
