from app.state_store import SQLiteStateStore
from app.resume import ResumableWorkflow

def test_resume_skips_completed_steps(tmp_path):
    store = SQLiteStateStore(str(tmp_path / "state.db"))
    calls = []
    steps = [("one", lambda s: calls.append("one") or 1), ("two", lambda s: calls.append("two") or s["one"] + 1)]
    first = ResumableWorkflow(store, steps).run("job")
    second = ResumableWorkflow(store, steps).run("job")
    assert first.completed == ("one", "two")
    assert second.resumed and calls == ["one", "two"]
    store.close()

def test_initial_state_used_for_new_workflow(tmp_path):
    store = SQLiteStateStore(str(tmp_path / "state.db"))
    result = ResumableWorkflow(store, [("sum", lambda s: s["x"] + 2)]).run("job", {"x": 3})
    assert result.outputs["sum"] == 5
    store.close()

def test_definition_mismatch_rejected(tmp_path):
    store = SQLiteStateStore(str(tmp_path / "state.db"))
    ResumableWorkflow(store, [("a", lambda s: 1)]).run("job")
    import pytest
    with pytest.raises(ValueError):
        ResumableWorkflow(store, [("b", lambda s: 2)]).run("job")
    store.close()
