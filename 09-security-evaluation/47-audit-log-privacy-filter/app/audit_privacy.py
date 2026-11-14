"""Redact sensitive fields and obvious credential-like values in audit records."""
import re
from typing import Any
_SECRET=re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+/-]+=*|((?:api[_-]?key|token|password|secret)\s*[:=]\s*)[^\s,;]+")
def _clean(value:Any,fields:set[str])->Any:
 if isinstance(value,dict):
  return {k:("[REDACTED]" if k.casefold() in fields else _clean(v,fields)) for k,v in value.items()}
 if isinstance(value,list): return [_clean(v,fields) for v in value]
 if isinstance(value,str): return _SECRET.sub(lambda m:(m.group(1) or m.group(2) or "")+"[REDACTED]",value)
 return value
def filter_audit_event(event:dict[str,Any],*,sensitive_fields:set[str]|None=None)->dict[str,Any]:
 if not isinstance(event,dict): raise TypeError("event must be a dictionary")
 fields={x.casefold() for x in (sensitive_fields or {"email","phone","authorization","api_key","password","token","secret"})}
 if any(not isinstance(x,str) or not x for x in fields): raise ValueError("sensitive field names must be non-empty strings")
 return _clean(event,fields)
