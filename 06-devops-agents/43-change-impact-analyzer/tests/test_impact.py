from app.impact import analyze_change_impact
import pytest

def test_finds_downstream_dependents():
    result=analyze_change_impact({"api":["worker"],"worker":["db"],"db":[]},["db"])
    assert result.affected_services==("api","worker")

def test_rejects_unknown_component():
    with pytest.raises(ValueError): analyze_change_impact({"api":[]},["missing"])
