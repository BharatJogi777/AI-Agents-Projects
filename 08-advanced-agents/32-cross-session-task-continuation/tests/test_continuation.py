import pytest
from app.continuation import TaskSnapshot, validate_resume

def test_resumes_paused_task_when_context_is_available():
    snap=TaskSnapshot("t1",1,"paused","step-3",("repo",))
    assert validate_resume(snap,available_context={"repo"}) == (True,())

def test_reports_missing_context_and_version_mismatch():
    snap=TaskSnapshot("t1",1,"paused","step",("repo","credentials"))
    ok,reasons=validate_resume(snap,available_context={"repo"})
    assert not ok and "missing_context:credentials" in reasons
    assert validate_resume(snap,available_context={"repo"},supported_version=2)[0] is False

def test_rejects_invalid_status_and_completed_task():
    with pytest.raises(ValueError): validate_resume(TaskSnapshot("t",1,"unknown","",()),available_context=set())
    assert validate_resume(TaskSnapshot("t",1,"completed","",()),available_context=set())[0] is False
