from dataclasses import dataclass
@dataclass(frozen=True)
class Step:id:str;action:str;depends_on:tuple[str,...]=();risk:str="low"
@dataclass(frozen=True)
class Validation:valid:bool;errors:tuple[str,...]
def validate_plan(steps,max_steps=20,allowed_risks=("low","medium")):
 e=[];ids=[s.id for s in steps];known=set(ids)
 if not steps or len(steps)>max_steps:e.append("step_count_out_of_bounds")
 if any(not x for x in ids) or len(ids)!=len(known):e.append("duplicate_or_empty_ids")
 for s in steps:
  if not s.action.strip() or len(s.action)>500:e.append("invalid_action:"+s.id)
  if s.risk not in allowed_risks:e.append("risk_not_allowed:"+s.id)
  if len(set(s.depends_on))!=len(s.depends_on) or any(d not in known for d in s.depends_on):e.append("invalid_dependencies:"+s.id)
 graph={s.id:s.depends_on for s in steps};vis=set();done=set()
 def visit(k):
  if k in vis:raise ValueError()
  if k in done:return
  vis.add(k)
  for d in graph.get(k,()):visit(d)
  vis.remove(k);done.add(k)
 try:
  for k in graph:visit(k)
 except ValueError:e.append("dependency_cycle")
 return Validation(not e,tuple(dict.fromkeys(e)))
