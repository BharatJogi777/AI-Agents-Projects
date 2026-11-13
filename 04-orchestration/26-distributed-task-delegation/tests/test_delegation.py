import pytest
from app.delegation import Worker, Task, Status, DelegationCoordinator

def test_delegate_and_complete():
    c = DelegationCoordinator({"w1": Worker("w1", frozenset({"search"}))})
    c.submit(Task("t1", frozenset({"search"}), {"q": "x"}))
    assert c.delegate("t1") == "w1"
    c.complete("t1", "w1", {"items": 1})
    assert c.tasks["t1"].status == Status.SUCCEEDED

def test_capacity_and_retry_limit():
    c = DelegationCoordinator({"w": Worker("w", frozenset({"x"}), 1)})
    c.submit(Task("a", frozenset({"x"}), {}, max_attempts=1))
    c.submit(Task("b", frozenset({"x"}), {}))
    c.delegate("a")
    with pytest.raises(RuntimeError): c.delegate("b")
    c.reject("a", "w", "temporary")
    assert c.tasks["a"].status == Status.FAILED
    with pytest.raises(RuntimeError): c.delegate("b")

def test_wrong_worker_cannot_complete():
    c = DelegationCoordinator({"w": Worker("w", frozenset({"x"}))})
    c.submit(Task("a", frozenset({"x"}), {})); c.delegate("a")
    with pytest.raises(ValueError): c.complete("a", "intruder", 1)
