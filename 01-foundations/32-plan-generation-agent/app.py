from dataclasses import dataclass,asdict
from typing import Protocol
import json
@dataclass(frozen=True)
class PlanStep:id:str;action:str;expected_outcome:str
@dataclass(frozen=True)
class Plan:objective:str;steps:tuple[PlanStep,...]
class Planner(Protocol):
 def generate(self,objective:str)->list[PlanStep]:...
class PlanGenerationAgent:
 def __init__(self,planner,max_steps=12):self.planner=planner;self.max_steps=max_steps
 def generate(self,objective):
  if not objective.strip() or len(objective)>2000:raise ValueError("invalid objective")
  steps=self.planner.generate(objective)
  if not 1<=len(steps)<=self.max_steps:raise ValueError("step count out of bounds")
  ids=set()
  for s in steps:
   if not s.id or s.id in ids or not s.action.strip() or not s.expected_outcome.strip() or max(len(s.action),len(s.expected_outcome))>500:raise ValueError("invalid step")
   ids.add(s.id)
  return Plan(objective,tuple(steps))
def to_json(p):return json.dumps(asdict(p),sort_keys=True)
def from_json(raw):
 try:d=json.loads(raw)
 except (ValueError,TypeError) as e:raise ValueError("invalid JSON") from e
 if not isinstance(d,dict) or set(d)!={"objective","steps"} or not isinstance(d["objective"],str) or not isinstance(d["steps"],list):raise ValueError("invalid plan shape")
 steps=[]
 for x in d["steps"]:
  if not isinstance(x,dict) or set(x)!={"id","action","expected_outcome"} or not all(isinstance(v,str) for v in x.values()):raise ValueError("invalid step")
  steps.append(PlanStep(**x))
 class P:
  def generate(self,_):return steps
 return PlanGenerationAgent(P()).generate(d["objective"])
