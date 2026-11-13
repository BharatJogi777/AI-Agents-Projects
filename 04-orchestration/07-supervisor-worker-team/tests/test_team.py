import pytest
from app.team import Assignment, SupervisorTeam

def test_supervisor_routes_to_allowlisted_worker():
    team = SupervisorTeam({"math": lambda task: "calculated"}, lambda task, names: Assignment("math", task))
    assert team.run("compute").output == "calculated"

def test_unknown_worker_fails_closed():
    team = SupervisorTeam({"math": lambda task: 1}, lambda task, names: Assignment("admin", task))
    assert team.run("do work").error

def test_worker_failure_is_reported():
    team = SupervisorTeam({"x": lambda task: 1 / 0}, lambda task, names: Assignment("x", task))
    assert team.run("task").error

def test_empty_task_rejected():
    team = SupervisorTeam({"x": str}, lambda task, names: Assignment("x", task))
    with pytest.raises(ValueError): team.run(" ")
