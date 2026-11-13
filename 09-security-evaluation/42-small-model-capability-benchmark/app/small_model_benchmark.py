"""Score small-model task capability against explicit acceptance thresholds."""
from dataclasses import dataclass
from typing import Mapping
@dataclass(frozen=True)
class CapabilityResult:
 model:str; passed:int; total:int; failed_tasks:tuple[str,...]
 @property
 def pass_rate(self)->float:return self.passed/self.total if self.total else 0.0
def evaluate_capabilities(model:str,scores:Mapping[str,float],thresholds:Mapping[str,float])->CapabilityResult:
 if not model.strip() or not scores or set(scores)!=set(thresholds): raise ValueError("model and matching non-empty task maps required")
 failed=[]
 for task,score in scores.items():
  threshold=thresholds[task]
  if not task or any(not isinstance(x,(int,float)) or isinstance(x,bool) or not 0<=x<=1 for x in (score,threshold)): raise ValueError("scores and thresholds must be in [0,1]")
  if score<threshold:failed.append(task)
 return CapabilityResult(model,len(scores)-len(failed),len(scores),tuple(sorted(failed)))
