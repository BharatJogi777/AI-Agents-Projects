"""Evaluate a deterministic fallback chain from supplied attempt outcomes."""
from dataclasses import dataclass
from typing import Iterable
@dataclass(frozen=True)
class Attempt:
 provider:str; succeeded:bool; error_code:str|None=None
@dataclass(frozen=True)
class FallbackResult:
 selected_provider:str|None; attempts:int; exhausted:bool; skipped_after_success:tuple[str,...]
def evaluate_fallbacks(attempts:Iterable[Attempt])->FallbackResult:
 rows=tuple(attempts)
 if not rows or any(not x.provider.strip() for x in rows):raise ValueError("at least one named provider required")
 names=[x.provider for x in rows]
 if len(names)!=len(set(names)):raise ValueError("providers must be unique")
 if any(not isinstance(x.succeeded,bool) for x in rows):raise ValueError("succeeded must be boolean")
 for i,x in enumerate(rows):
  if x.succeeded:
   return FallbackResult(x.provider,i+1,False,tuple(names[i+1:]))
 return FallbackResult(None,len(rows),True,())
