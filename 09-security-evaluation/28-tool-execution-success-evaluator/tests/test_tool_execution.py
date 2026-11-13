import pytest
from app.tool_execution import evaluate_executions

def test_mixed_results():
    r=evaluate_executions([True,False,True])
    assert r.success_rate == pytest.approx(2/3) and r.failure_indices == (1,)

def test_empty_run():
    assert evaluate_executions([]).success_rate == 0

def test_all_successful():
    assert evaluate_executions([True,True]).failed == 0

def test_rejects_non_boolean_values():
    with pytest.raises(ValueError): evaluate_executions([1,False])
