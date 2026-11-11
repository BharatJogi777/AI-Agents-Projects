from dataclasses import dataclass
from collections.abc import Sequence
@dataclass(frozen=True)
class Source: id:str; text:str
@dataclass(frozen=True)
class Claim: text:str; source_ids:tuple[str,...]
@dataclass(frozen=True)
class GroundedAnswer: answer:str; claims:tuple[Claim,...]; source_ids:tuple[str,...]
def build_grounded_answer(claims:Sequence[Claim],sources:Sequence[Source])->GroundedAnswer:
 source_map={s.id:s for s in sources}
 if len(source_map)!=len(sources) or any(not s.id or not s.text.strip() for s in sources): raise ValueError("sources need unique IDs and non-empty text")
 if not claims: raise ValueError("at least one claim is required")
 lines=[]; used=[]
 for claim in claims:
  if not claim.text.strip() or not claim.source_ids: raise ValueError("each claim needs text and citations")
  if len(set(claim.source_ids))!=len(claim.source_ids): raise ValueError("duplicate citation on claim")
  unknown=set(claim.source_ids)-source_map.keys()
  if unknown: raise ValueError(f"unknown source IDs: {sorted(unknown)}")
  refs=", ".join(f"[{sid}]" for sid in claim.source_ids); lines.append(f"{claim.text} {refs}")
  for sid in claim.source_ids:
   if sid not in used: used.append(sid)
 return GroundedAnswer("\n".join(lines),tuple(claims),tuple(used))
