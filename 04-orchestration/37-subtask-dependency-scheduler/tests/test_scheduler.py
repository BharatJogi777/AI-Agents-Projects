import pytest
from app.scheduler import DependencyScheduler

def test_topological_order_and_ready_tasks():
    s=DependencyScheduler(); s.add("build"); s.add("test",{"build"}); s.add("deploy",{"test"})
    assert s.order() == ["build","test","deploy"]
    assert s.ready(set()) == ["build"]
    assert s.ready({"build"}) == ["test"]

def test_cycle_and_unknown_dependency():
    s=DependencyScheduler(); s.add("a",{"b"}); s.add("b",{"a"})
    with pytest.raises(RuntimeError): s.order()
    t=DependencyScheduler(); t.add("x",{"missing"})
    with pytest.raises(ValueError): t.order()
