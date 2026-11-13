"""Create ordered, risk-aware refactoring work items."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Step:
    title:str
    rationale:str
    risk:str
    verification:str
def plan(target:str, goals:list[str], constraints:list[str]|None=None)->list[Step]:
    if not isinstance(target,str) or not target.strip(): raise ValueError("target is required")
    if not goals or any(not isinstance(x,str) or not x.strip() for x in goals): raise ValueError("At least one non-empty goal is required")
    if constraints is not None and any(not isinstance(x,str) or not x.strip() for x in constraints): raise ValueError("Constraints must be non-empty strings")
    steps=[Step("Establish baseline",f"Capture behavior and performance for {target}","low","Run existing tests and record baseline metrics")]
    steps.extend(Step("Address: "+g.strip(),"Make one focused change toward "+g.strip(),"medium","Add focused tests and inspect diff") for g in goals)
    steps.extend([Step("Run compatibility checks","Confirm public behavior and integrations remain stable","high","Run full tests and contract checks"),Step("Review and stage rollout","Keep deployment reversible and observable","medium","Stage rollout, monitor metrics, define rollback")])
    return steps
