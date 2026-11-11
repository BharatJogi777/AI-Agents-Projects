import pytest
from app import *
def test_step_and_cost():
 b=RunBudget(Budget(1,10,1),clock=lambda:0); b.consume(.5)
 with pytest.raises(BudgetExceeded) as e: b.consume()
 assert e.value.reason is StopReason.STEPS
 c=RunBudget(Budget(5,10,1),clock=lambda:0)
 with pytest.raises(BudgetExceeded) as e: c.consume(2)
 assert e.value.reason is StopReason.COST and c.steps==0
def test_deadline():
 ticks=iter([0,2]); b=RunBudget(Budget(2,1,1),clock=lambda:next(ticks))
 with pytest.raises(BudgetExceeded) as e: b.consume()
 assert e.value.reason is StopReason.TIME
