import pytest
from app.small_model_benchmark import evaluate_capabilities
def test_capability_thresholds():
 r=evaluate_capabilities("compact",{"json":.9,"tools":.6,"reasoning":.8},{"json":.8,"tools":.7,"reasoning":.8})
 assert r.passed==2 and r.failed_tasks==("tools",)
def test_empty_or_mismatched_tasks_rejected():
 with pytest.raises(ValueError): evaluate_capabilities("m",{}, {})
 with pytest.raises(ValueError): evaluate_capabilities("m",{"a":.5},{"b":.5})
