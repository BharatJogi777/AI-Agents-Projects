import json,re
from typing import Any,Callable
from .contracts import FunctionCall,FunctionCallError
_NAME=re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]{0,63}$")
def parse_function_call(payload:dict[str,Any],*,allowed_names:set[str],max_argument_chars:int=16000)->FunctionCall:
    if not isinstance(payload,dict): raise FunctionCallError("call must be an object")
    if type(max_argument_chars) is not int or max_argument_chars<1: raise ValueError("max_argument_chars must be positive")
    call_id=payload.get("id",""); function=payload.get("function")
    if not isinstance(call_id,str) or not call_id or len(call_id)>128: raise FunctionCallError("invalid call id")
    if not isinstance(function,dict): raise FunctionCallError("function must be an object")
    name,raw=function.get("name"),function.get("arguments")
    if not isinstance(name,str) or not _NAME.fullmatch(name): raise FunctionCallError("invalid function name")
    if name not in allowed_names: raise FunctionCallError("function is not allowlisted")
    if isinstance(raw,str):
        if len(raw.encode("utf-8"))>max_argument_chars: raise FunctionCallError("arguments exceed size limit")
        try: args=json.loads(raw)
        except (json.JSONDecodeError,UnicodeError) as exc: raise FunctionCallError("arguments are not valid JSON") from exc
    else: args=raw
    if not isinstance(args,dict): raise FunctionCallError("arguments must decode to an object")
    try: encoded=json.dumps(args,ensure_ascii=False,allow_nan=False).encode("utf-8")
    except (TypeError,ValueError) as exc: raise FunctionCallError("arguments must contain JSON values only") from exc
    if len(encoded)>max_argument_chars: raise FunctionCallError("arguments exceed size limit")
    return FunctionCall(call_id,name,args)
def dispatch_function_call(call:FunctionCall,handlers:dict[str,Callable[[dict[str,Any]],Any]])->Any:
    handler=handlers.get(call.name)
    if handler is None: raise FunctionCallError("no handler registered for allowlisted function")
    try: return handler(call.arguments)
    except Exception as exc: raise FunctionCallError("function handler failed") from exc
