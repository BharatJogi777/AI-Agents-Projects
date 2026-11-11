import pytest
from plan_tracker import *
def test_dependencies_failure_recovery_and_snapshot():
 t=ExecutionTracker([StepState("a"),StepState("b",("a",))])
 with pytest.raises(ValueError):t.transition("b",Status.RUNNING)
 t.transition("a",Status.RUNNING);t.transition("a",Status.FAILED,error="provider timeout")
 t.transition("a",Status.PENDING);t.transition("a",Status.RUNNING);t.transition("a",Status.SUCCEEDED)
 t.transition("b",Status.RUNNING);t.transition("b",Status.SUCCEEDED)
 assert t.snapshot()["b"]["status"]=="succeeded"
def test_completion_idempotent_but_illegal_transition_rejected():
 t=ExecutionTracker([StepState("a")]);t.transition("a",Status.RUNNING);t.transition("a",Status.SUCCEEDED)
 assert t.transition("a",Status.SUCCEEDED).status==Status.SUCCEEDED
 with pytest.raises(ValueError):t.transition("a",Status.RUNNING)
