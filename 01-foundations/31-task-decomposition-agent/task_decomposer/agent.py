from typing import Protocol
from .contracts import Task
from .validator import validate_tasks
class Decomposer(Protocol):
    def decompose(self,objective:str)->list[Task]: ...
class TaskDecompositionAgent:
    def __init__(self,planner:Decomposer,max_tasks:int=30,max_objective_chars:int=2000):
        if type(max_objective_chars) is not int or max_objective_chars<1: raise ValueError("objective limit must be positive")
        self.planner=planner;self.max_tasks=max_tasks;self.max_objective_chars=max_objective_chars
    def run(self,objective:str)->tuple[Task,...]:
        if not isinstance(objective,str) or not objective.strip() or len(objective)>self.max_objective_chars: raise ValueError("invalid objective")
        tasks=self.planner.decompose(objective)
        return validate_tasks(tasks,self.max_tasks)
