import pytest
from app import *
def test_dependency_flow():
 t=ExecutionTracker([StepState("a"),StepState("b",("a",))])
 with pytest.raises(ValueError):t.transition("b",Status.RUNNING)
 t.transition("a",Status.RUNNING);t.transition("a",Status.SUCCEEDED);assert t.ready("b")
 t.transition("b",Status.RUNNING);t.transition("b",Status.SUCCEEDED);assert t.snapshot()["b"]=="succeeded"
def test_illegal(): 
 with pytest.raises(ValueError):ExecutionTracker([StepState("a")]).transition("a",Status.SUCCEEDED)
