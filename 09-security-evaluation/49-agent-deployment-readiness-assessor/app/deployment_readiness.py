"""Assess a deployment checklist; missing evidence blocks readiness."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Gate:
 name:str; passed:bool; evidence_ref:str|None=None
@dataclass(frozen=True)
class Readiness:
 ready:bool; passed:int; total:int; blockers:tuple[str,...]; missing_evidence:tuple[str,...]
def assess_readiness(gates:list[Gate],*,required_gates:set[str])->Readiness:
 names=[g.name for g in gates]
 if any(not x for x in names) or len(names)!=len(set(names)): raise ValueError("gate names must be unique and non-empty")
 if any(not isinstance(g.passed,bool) for g in gates): raise ValueError("gate passed values must be boolean")
 by_name={g.name:g for g in gates}; blockers=[]; missing=[]
 for name in sorted(required_gates):
  gate=by_name.get(name)
  if gate is None: blockers.append(name); missing.append(name)
  elif not gate.passed: blockers.append(name)
  elif not gate.evidence_ref: blockers.append(name); missing.append(name)
 passed=sum(1 for g in gates if g.passed and g.evidence_ref)
 return Readiness(not blockers,passed,len(required_gates),tuple(blockers),tuple(missing))
