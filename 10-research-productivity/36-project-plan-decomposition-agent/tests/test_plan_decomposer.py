from app.plan_decomposer import Task, decompose_plan
import pytest

def test_topological_order_is_stable():
    tasks=[Task("b","Build",("a",)),Task("a","Plan"),Task("c","Review",("b",))]
    assert [t.id for t in decompose_plan(tasks)] == ["a","b","c"]

def test_cycle_rejected():
    with pytest.raises(ValueError, match="cycle"):
        decompose_plan([Task("a","A",("b",)),Task("b","B",("a",))])

def test_unknown_dependency_rejected():
    with pytest.raises(ValueError, match="unknown"):
        decompose_plan([Task("a","A",("missing",))])
