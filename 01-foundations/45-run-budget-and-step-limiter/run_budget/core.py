from dataclasses import dataclass
from enum import Enum
from threading import Lock
from time import monotonic
import math
class StopReason(str,Enum):STEPS="max_steps";TIME="deadline";COST="cost_limit"
class BudgetExceeded(RuntimeError):
 def __init__(self,reason):self.reason=reason;super().__init__(reason.value)
@dataclass(frozen=True)
class Budget:
 max_steps:int;max_seconds:float;max_cost:float
 def __post_init__(self):
  if isinstance(self.max_steps,bool) or self.max_steps<1:raise ValueError("max_steps must be >=1")
  if not math.isfinite(self.max_seconds) or self.max_seconds<=0 or not math.isfinite(self.max_cost) or self.max_cost<0:raise ValueError("invalid time/cost budget")
@dataclass(frozen=True)
class Snapshot:
 steps:int;cost:float;elapsed:float;remaining_steps:int;remaining_cost:float
class RunBudget:
 def __init__(self,budget,clock=monotonic):
  self.budget=budget;self._clock=clock;self._started=clock();self._steps=0;self._cost=0.0;self._lock=Lock()
 @property
 def steps(self):
  with self._lock:return self._steps
 @property
 def cost(self):
  with self._lock:return self._cost
 def check(self):
  with self._lock:
   if self._clock()-self._started>=self.budget.max_seconds:raise BudgetExceeded(StopReason.TIME)
 def consume(self,estimated_cost=0.0):
  if isinstance(estimated_cost,bool) or not isinstance(estimated_cost,(int,float)) or not math.isfinite(estimated_cost) or estimated_cost<0:raise ValueError("cost must be finite and non-negative")
  with self._lock:
   if self._clock()-self._started>=self.budget.max_seconds:raise BudgetExceeded(StopReason.TIME)
   if self._steps>=self.budget.max_steps:raise BudgetExceeded(StopReason.STEPS)
   if self._cost+estimated_cost>self.budget.max_cost:raise BudgetExceeded(StopReason.COST)
   self._steps+=1;self._cost+=estimated_cost
 def snapshot(self):
  with self._lock:
   elapsed=max(0.0,self._clock()-self._started)
   return Snapshot(self._steps,self._cost,elapsed,max(0,self.budget.max_steps-self._steps),max(0.0,self.budget.max_cost-self._cost))
