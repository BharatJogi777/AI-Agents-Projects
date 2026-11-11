"""Validate and normalize provider function/tool call payloads before dispatch."""
import json
import re
from dataclasses import dataclass
from typing import Any,Callable

_NAME=re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]{0,63}$")

class FunctionCallError(ValueError): pass

@dataclass(frozen=True)
class FunctionCall:
    call_id:str
    name:str
    arguments:dict[str,Any]

def parse_function_call(payload:dict[str,Any],*,allowed_names:set[str],max_argument_chars:int=16_000)->FunctionCall:
    if not isinstance(payload,dict): raise FunctionCallError("call must be an object")
    call_id=payload.get("id","")
    function=payload.get("function")
    if not isinstance(call_id,str) or not call_id or len(call_id)>128: raise FunctionCallError("invalid call id")
    if not isinstance(function,dict): raise FunctionCallError("function must be an object")
    name=function.get("name"); raw=function.get("arguments")
    if not isinstance(name,str) or not _NAME.fullmatch(name): raise FunctionCallError("invalid function name")
    if name not in allowed_names: raise FunctionCallError("function is not allowlisted")
    if isinstance(raw,str):
        if len(raw)>max_argument_chars: raise FunctionCallError("arguments exceed size limit")
        try: args=json.loads(raw)
        except json.JSONDecodeError as exc: raise FunctionCallError("arguments are not valid JSON") from exc
    else: args=raw
    if not isinstance(args,dict): raise FunctionCallError("arguments must decode to an object")
    return FunctionCall(call_id,name,args)

def dispatch_function_call(call:FunctionCall,handlers:dict[str,Callable[[dict[str,Any]],Any]])->Any:
    handler=handlers.get(call.name)
    if handler is None: raise FunctionCallError("no handler registered for allowlisted function")
    return handler(call.arguments)
