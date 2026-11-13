from app.graph import build_dependency_map, downstream, upstream
import pytest

def test_builds_dependency_graph_and_detects_cycle():
    report=build_dependency_map([("api","orders"),("orders","db"),("db","api")])
    assert report.cycles
    assert downstream(report,"api")=={"orders","db"}
    assert upstream(report,"db")=={"api","orders"}

def test_rejects_self_dependency():
    with pytest.raises(ValueError): build_dependency_map([("api","api")])
