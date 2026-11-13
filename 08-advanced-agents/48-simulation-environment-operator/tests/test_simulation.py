import pytest
from app.simulation import Command, build_plan

def test_builds_dry_run_plan():
    plan=build_plan([Command("run_steps",(("steps","5"),))],allowed_parameters=set())
    assert plan[0]["status"]=="not_executed"

def test_rejects_unapproved_parameter_and_bad_step_count():
    with pytest.raises(ValueError):
        build_plan([Command("set_parameter",(("admin","true"),))],allowed_parameters={"speed"})
    with pytest.raises(ValueError):
        build_plan([Command("run_steps",(("steps","0"),))],allowed_parameters=set())
