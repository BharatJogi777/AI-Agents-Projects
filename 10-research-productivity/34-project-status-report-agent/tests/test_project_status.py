import pytest
from app.project_status import build_status_report

def test_builds_status_report_from_facts():
    r=build_status_report(project="Migration",overall_status="at_risk",completed=["Design"],in_progress=["API"],blocked=["Vendor"],next_steps=["Escalate"])
    assert r.blocked==("Vendor",) and r.overall_status=="at_risk"

def test_rejects_unknown_status():
    with pytest.raises(ValueError):
        build_status_report(project="X",overall_status="green",completed=[],in_progress=[],blocked=[],next_steps=[])
