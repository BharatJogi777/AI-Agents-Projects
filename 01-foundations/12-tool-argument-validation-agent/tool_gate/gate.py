from __future__ import annotations
import json
from typing import Any, Callable
from pydantic import BaseModel, ValidationError
from .errors import ToolCallRejected, ToolHandlerFailed

class ArgumentGate:
    """Validate untrusted tool-call envelopes before trusted handler dispatch."""
    def __init__(self,schemas:dict[str,type[BaseModel]],handlers:dict[str,Callable],*,max_argument_bytes:int=16384,max_feedback_items:int=8):
        if not schemas or set(schemas)!=set(handlers): raise ValueError("each registered schema must have exactly one handler")
        if any(not isinstance(m,type) or not issubclass(m,BaseModel) for m in schemas.values()): raise ValueError("all schemas must be Pydantic model classes")
        if not 128<=max_argument_bytes<=1000000: raise ValueError("max_argument_bytes must be 128..1000000")
        if not 1<=max_feedback_items<=20: raise ValueError("max_feedback_items must be 1..20")
        self._schemas,self._handlers=dict(schemas),dict(handlers)
        self._max_bytes,self._max_feedback=max_argument_bytes,max_feedback_items
    def validate(self,name:str,raw:Any)->BaseModel:
        model=self._schemas.get(name)
        if model is None: raise ToolCallRejected("tool is not allowlisted")
        if isinstance(raw,str):
            if len(raw.encode("utf-8"))>self._max_bytes: raise ToolCallRejected("tool arguments exceed size limit")
            try: raw=json.loads(raw)
            except (json.JSONDecodeError,UnicodeError) as exc: raise ToolCallRejected("arguments are not valid JSON") from exc
        if not isinstance(raw,dict): raise ToolCallRejected("arguments must be a JSON object")
        try: encoded=json.dumps(raw,ensure_ascii=False,allow_nan=False).encode("utf-8")
        except (TypeError,ValueError) as exc: raise ToolCallRejected("arguments must contain JSON values only") from exc
        if len(encoded)>self._max_bytes: raise ToolCallRejected("tool arguments exceed size limit")
        try: return model.model_validate(raw,strict=True)
        except ValidationError as exc:
            issues=[{"path":".".join(str(p) for p in e["loc"])[:160],"type":e["type"],"message":e["msg"][:120]} for e in exc.errors()[:self._max_feedback]]
            raise ToolCallRejected(json.dumps({"validation_errors":issues})) from exc
    def execute(self,name:str,raw:Any)->dict[str,Any]:
        args=self.validate(name,raw)
        try: return {"ok":True,"result":self._handlers[name](args)}
        except Exception as exc: raise ToolHandlerFailed(f"trusted handler failed: {name}") from exc
    def validate_and_execute(self,name:str,raw:Any)->dict[str,Any]:
        """Compatibility name used by the first tutorial revision."""
        return self.execute(name,raw)
    def schemas(self)->dict[str,type[BaseModel]]: return dict(self._schemas)
