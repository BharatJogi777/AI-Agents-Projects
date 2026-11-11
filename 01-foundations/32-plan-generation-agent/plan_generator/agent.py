from typing import Protocol
from .contracts import Plan,PlanStep
from .serialization import PlanFormatError
class Planner(Protocol):
    def generate(self,objective:str)->list[PlanStep]: ...
class PlanGenerationAgent:
    def __init__(self,planner:Planner,max_steps:int=12,max_objective_chars:int=2000):
        if type(max_steps) is not int or max_steps<1:raise ValueError("max_steps must be positive")
        self.planner=planner;self.max_steps=max_steps;self.max_objective_chars=max_objective_chars
    def generate(self,objective:str)->Plan:
        if not isinstance(objective,str) or not objective.strip() or len(objective)>self.max_objective_chars:raise ValueError("invalid objective")
        steps=self.planner.generate(objective)
        if not isinstance(steps,(list,tuple)) or not 1<=len(steps)<=self.max_steps:raise PlanFormatError("step count out of bounds")
        ids=set()
        for s in steps:
            if not isinstance(s,PlanStep) or any(not isinstance(v,str) or not v.strip() for v in (s.id,s.action,s.expected_outcome)):raise PlanFormatError("invalid step fields")
            if len(s.id)>80 or len(s.action)>500 or len(s.expected_outcome)>500 or s.id in ids:raise PlanFormatError("duplicate or oversized step")
            ids.add(s.id)
        return Plan(objective,tuple(steps))
