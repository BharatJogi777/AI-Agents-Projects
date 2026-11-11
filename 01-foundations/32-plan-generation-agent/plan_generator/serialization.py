import json
from .contracts import Plan,PlanStep
class PlanFormatError(ValueError):pass
def to_json(plan:Plan)->str:
    if not isinstance(plan,Plan):raise TypeError("plan must be Plan")
    return json.dumps({"objective":plan.objective,"steps":[{"id":s.id,"action":s.action,"expected_outcome":s.expected_outcome} for s in plan.steps]},ensure_ascii=False,sort_keys=True,separators=(",",":"))
def from_json(raw:str,max_steps:int=12)->Plan:
    if type(max_steps) is not int or max_steps<1:raise ValueError("max_steps must be positive")
    try:data=json.loads(raw)
    except (TypeError,json.JSONDecodeError) as exc:raise PlanFormatError("invalid plan JSON") from exc
    if not isinstance(data,dict) or set(data)!={"objective","steps"} or not isinstance(data["objective"],str) or not data["objective"].strip() or len(data["objective"])>2000 or not isinstance(data["steps"],list):raise PlanFormatError("invalid plan shape")
    if not 1<=len(data["steps"])<=max_steps:raise PlanFormatError("step count out of bounds")
    steps=[];ids=set()
    for item in data["steps"]:
        if not isinstance(item,dict) or set(item)!={"id","action","expected_outcome"} or any(not isinstance(v,str) or not v.strip() for v in item.values()):raise PlanFormatError("invalid step shape")
        step=PlanStep(**item)
        if len(step.id)>80 or len(step.action)>500 or len(step.expected_outcome)>500 or step.id in ids:raise PlanFormatError("duplicate or oversized step")
        ids.add(step.id);steps.append(step)
    return Plan(data["objective"],tuple(steps))
