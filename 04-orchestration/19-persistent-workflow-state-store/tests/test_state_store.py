import pytest
from app.state_store import SQLiteStateStore

def test_save_load_and_update(tmp_path):
    store = SQLiteStateStore(str(tmp_path / "state.db"))
    first = store.save("wf-1", {"step": 1})
    assert first.version == 1
    assert store.load("wf-1").state == {"step": 1}
    second = store.save("wf-1", {"step": 2}, expected_version=1)
    assert second.version == 2 and store.load("wf-1").state["step"] == 2
    store.close()

def test_optimistic_version_conflict(tmp_path):
    store = SQLiteStateStore(str(tmp_path / "state.db"))
    store.save("wf", {"x": 1})
    with pytest.raises(RuntimeError): store.save("wf", {"x": 2}, expected_version=0)
    store.close()

def test_missing_workflow_returns_none(tmp_path):
    store = SQLiteStateStore(str(tmp_path / "state.db"))
    assert store.load("missing") is None
    store.close()
