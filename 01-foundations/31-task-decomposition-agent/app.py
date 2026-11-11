from dataclasses import dataclass
from typing import Protocol
@dataclass(frozen=True)
class Task:id:str;description:str;depends_on:tuple[str,...]=()
class Decomposer(Protocol):
 def decompose(self,objective:str)->list[Task]:...
def validate_tasks(tasks,max_tasks=30):
 if not tasks or len(tasks)>max_tasks:raise ValueError("task count out of bounds")
 by={}
 for t in tasks:
  if not t.id or t.id in by or not t.description.strip() or len(t.description)>500:raise ValueError("invalid task")
  by[t.id]=t
 for t in tasks:
  if t.id in t.depends_on or len(set(t.depends_on))!=len(t.depends_on) or any(d not in by for d in t.depends_on):raise ValueError("invalid dependency")
 visiting=set();done=set()
 def visit(k):
  if k in visiting:raise ValueError("dependency cycle")
  if k in done:return
  visiting.add(k)
  for d in by[k].depends_on:visit(d)
  visiting.remove(k);done.add(k)
 for k in by:visit(k)
 return tasks
class TaskDecompositionAgent:
 def __init__(self,planner,max_tasks=30):self.planner=planner;self.max_tasks=max_tasks
 def run(self,objective):
  if not objective.strip() or len(objective)>2000:raise ValueError("invalid objective")
  return validate_tasks(self.planner.decompose(objective),self.max_tasks)
