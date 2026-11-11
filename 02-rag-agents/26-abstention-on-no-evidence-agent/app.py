from dataclasses import dataclass
from collections.abc import Sequence
@dataclass(frozen=True)
class RetrievedEvidence: source_id:str; text:str; score:float
@dataclass(frozen=True)
class AnswerDecision: answer:str|None; abstained:bool; reason:str; source_ids:tuple[str,...]
def decide_answer(evidence:Sequence[RetrievedEvidence],minimum_score:float=.35,minimum_sources:int=1)->AnswerDecision:
 if not 0<=minimum_score<=1 or minimum_sources<1: raise ValueError("invalid evidence policy")
 eligible=[]; seen=set()
 for item in evidence:
  if not item.source_id or not item.text.strip(): continue
  if isinstance(item.score,bool) or not isinstance(item.score,(int,float)) or not 0<=item.score<=1: raise ValueError("evidence scores must be in [0, 1]")
  if item.score>=minimum_score and item.source_id not in seen: eligible.append(item); seen.add(item.source_id)
 if len(eligible)<minimum_sources: return AnswerDecision(None,True,"insufficient supporting evidence",())
 return AnswerDecision(None,False,"evidence available; answer generation may proceed",tuple(x.source_id for x in eligible))
