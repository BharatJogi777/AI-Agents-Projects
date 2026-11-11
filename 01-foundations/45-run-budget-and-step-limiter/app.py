"""AG-045: Run budget and step limiter. Enforce independent maximum-step, elapsed-time, and estimated-cost budgets with explicit stop reasons."""
from dataclasses import dataclass
from enum import Enum
from time import monotonic
class StopReason(str,Enum): STEPS="max_steps"; TIME="deadline"; COST="cost_limit"
class BudgetExceeded(RuntimeError):
 def __init__(self,reason): self.reason=reason; super().__init__(reason.value)
@dataclass(frozen=True)
class Budget:
 max_steps:int; max_seconds:float; max_cost:float
 def __post_init__(self):
  if self.max_steps<1 or self.max_seconds<=0 or self.max_cost<0: raise ValueError("invalid budget")
class RunBudget:
 def __init__(self,budget,clock=monotonic): self.budget=budget; self.clock=clock; self.start=clock(); self.steps=0; self.cost=0.0
 def check(self):
  if self.clock()-self.start>=self.budget.max_seconds: raise BudgetExceeded(StopReason.TIME)
 def consume(self,cost=0.0):
  if cost<0: raise ValueError("negative cost")
  self.check()
  if self.steps>=self.budget.max_steps: raise BudgetExceeded(StopReason.STEPS)
  if self.cost+cost>self.budget.max_cost: raise BudgetExceeded(StopReason.COST)
  self.steps+=1; self.cost+=cost; self.check()
