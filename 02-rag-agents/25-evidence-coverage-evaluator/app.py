from dataclasses import dataclass
from collections.abc import Sequence
@dataclass(frozen=True)
class ClaimEvidence: claim_id:str; claim:str; source_ids:tuple[str,...]
@dataclass(frozen=True)
class CoverageReport: total_claims:int; covered_claims:int; coverage:float; uncovered_ids:tuple[str,...]
def evaluate_coverage(claims:Sequence[ClaimEvidence],known_source_ids:set[str])->CoverageReport:
 ids=[c.claim_id for c in claims]
 if any(not i for i in ids) or len(set(ids))!=len(ids): raise ValueError("claim IDs must be non-empty and unique")
 if any(not c.claim.strip() for c in claims): raise ValueError("claim text is required")
 uncovered=[]; covered=0
 for c in claims:
  if c.source_ids and set(c.source_ids)<=known_source_ids: covered+=1
  else: uncovered.append(c.claim_id)
 total=len(claims)
 return CoverageReport(total,covered,covered/total if total else 1.0,tuple(uncovered))
