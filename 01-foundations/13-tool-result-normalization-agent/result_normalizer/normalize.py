import json,math
from datetime import date,datetime
from typing import Any
from .policy import NormalizationPolicy
SENSITIVE_KEYS={"password","passwd","token","access_token","refresh_token","secret","api_key","apikey","authorization","cookie","set-cookie"}

def _safe(value:Any,depth:int,policy:NormalizationPolicy,active:set[int],warnings:list[str])->Any:
    if depth>policy.max_depth: warnings.append("maximum nesting depth reached"); return "[DEPTH_LIMIT]"
    if value is None or isinstance(value,(bool,int)): return value
    if isinstance(value,float): return value if math.isfinite(value) else "[NON_FINITE_NUMBER]"
    if isinstance(value,str):
        if len(value)>policy.max_string_chars: warnings.append("string truncated"); return value[:policy.max_string_chars]+"…[TRUNCATED]"
        return value
    if isinstance(value,(datetime,date)): return value.isoformat()
    if isinstance(value,bytes): warnings.append("binary output represented as metadata"); return {"type":"bytes","length":len(value)}
    identity=id(value)
    if isinstance(value,dict):
        if identity in active: warnings.append("circular reference replaced"); return "[CIRCULAR_REFERENCE]"
        active.add(identity); out={}
        try:
            for i,(key,item) in enumerate(value.items()):
                if i>=policy.max_items_per_container:
                    warnings.append("mapping item limit reached"); out["_truncated_items"]=len(value)-i; break
                name=str(key)[:policy.max_string_chars]
                out[name]="[REDACTED]" if name.lower() in SENSITIVE_KEYS else _safe(item,depth+1,policy,active,warnings)
        finally: active.remove(identity)
        return out
    if isinstance(value,(list,tuple)):
        if identity in active: warnings.append("circular reference replaced"); return "[CIRCULAR_REFERENCE]"
        active.add(identity)
        try: out=[_safe(x,depth+1,policy,active,warnings) for x in value[:policy.max_items_per_container]]
        finally: active.remove(identity)
        if len(value)>policy.max_items_per_container:
            warnings.append("sequence item limit reached"); out.append(f"[{len(value)-policy.max_items_per_container} ITEMS OMITTED]")
        return out
    warnings.append(f"unsupported value type: {type(value).__name__}")
    return {"type":type(value).__name__,"repr":"[UNSUPPORTED]"}

def normalize_tool_result(result:Any,*,ok:bool=True,max_depth:int=6,max_string:int=4000,max_items:int=100,max_output_bytes:int=16000,policy:NormalizationPolicy|None=None)->dict[str,Any]:
    if policy is None:
        policy=NormalizationPolicy(max_depth=max_depth,max_string_chars=max_string,max_items_per_container=max_items,max_output_bytes=max_output_bytes)
    warnings=[]; data=_safe(result,0,policy,set(),warnings)
    envelope={"ok":bool(ok),"data":data,"warnings":list(dict.fromkeys(warnings))}
    encoded=json.dumps(envelope,ensure_ascii=False,separators=(",",":"),allow_nan=False)
    if len(encoded.encode("utf-8"))>policy.max_output_bytes:
        envelope["data"]={"type":"omitted","reason":"normalized output exceeded byte budget"}
        envelope["warnings"].append("output byte budget exceeded")
    return envelope
