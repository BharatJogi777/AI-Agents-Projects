import pytest
from run_budget import *
def test_step_and_cost_limits_are_independent():
 b=RunBudget(Budget(2,100,1.0));b.consume(.4);b.consume(.6)
 with pytest.raises(BudgetExceeded) as e:b.consume(0)
 assert e.value.reason is StopReason.STEPS
def test_cost_limit_does_not_consume_step():
 b=RunBudget(Budget(5,100,.5))
 with pytest.raises(BudgetExceeded) as e:b.consume(.6)
 assert e.value.reason is StopReason.COST and b.snapshot().steps==0
def test_deadline_uses_monotonic_clock():
 now=[0.0];b=RunBudget(Budget(5,2,1),clock=lambda:now[0]);b.consume(.1);now[0]=2
 with pytest.raises(BudgetExceeded) as e:b.consume(0)
 assert e.value.reason is StopReason.TIME
def test_snapshot_and_invalid_budget():
 b=RunBudget(Budget(3,10,2));b.consume(.5);s=b.snapshot()
 assert (s.steps,s.remaining_steps,s.remaining_cost)==(1,2,1.5)
 with pytest.raises(ValueError):Budget(0,1,1)
