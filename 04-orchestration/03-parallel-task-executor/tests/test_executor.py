import pytest
from app.executor import ParallelExecutor

def test_parallel_results_keep_input_order():
    results = ParallelExecutor(2).run({"a": lambda: 1, "b": lambda: 2})
    assert [(r.name, r.value) for r in results] == [("a", 1), ("b", 2)]

def test_task_failure_is_isolated():
    results = ParallelExecutor().run({"bad": lambda: 1 / 0, "good": lambda: "ok"})
    assert results[0].error
    assert results[1].value == "ok"

def test_worker_limit_validation():
    with pytest.raises(ValueError):
        ParallelExecutor(0)
