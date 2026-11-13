import pytest
from app.desktop import Step, validate_workflow, dry_run

def test_dry_run_only_creates_pending_plan():
    plan=dry_run([Step("open_document","report")],allowed_targets={"report"})
    assert plan[0]["status"]=="awaiting_user_approval"

def test_rejects_unapproved_target_and_long_wait():
    with pytest.raises(ValueError):
        validate_workflow([Step("open_document","/etc/passwd")],allowed_targets={"report"})
    with pytest.raises(ValueError):
        validate_workflow([Step("wait","timer","60")],allowed_targets={"timer"})
