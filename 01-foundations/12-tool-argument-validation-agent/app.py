import json
from typing import Any,Callable
from pydantic import BaseModel,ConfigDict,ValidationError

class ToolCallRejected(ValueError): pass

class SearchArgs(BaseModel):
    model_config=ConfigDict(extra="forbid",strict=True)
    query:str
    limit:int

def demo_search(args:SearchArgs)->dict[str,Any]:
    if not args.query.strip(): raise ValueError("query cannot be blank")
    if not 1<=args.limit<=20: raise ValueError("limit must be 1..20")
    return {"query":args.query,"limit":args.limit,"items":[]}

class ArgumentGate:
    def __init__(self,schemas:dict[str,type[BaseModel]],handlers:dict[str,Callable]):
        if set(schemas)!=set(handlers): raise ValueError("each schema must have exactly one handler")
        if any(not isinstance(m,type) or not issubclass(m,BaseModel) for m in schemas.values()):
            raise ValueError("all schemas must be Pydantic models")
        self.schemas,self.handlers=dict(schemas),dict(handlers)

    def validate_and_execute(self,name:str,raw:Any)->dict[str,Any]:
        model=self.schemas.get(name)
        if model is None: raise ToolCallRejected("tool is not allowlisted")
        if isinstance(raw,str):
            try: raw=json.loads(raw)
            except json.JSONDecodeError as exc: raise ToolCallRejected("arguments are not valid JSON") from exc
        if not isinstance(raw,dict): raise ToolCallRejected("arguments must be a JSON object")
        try: args=model.model_validate(raw)
        except ValidationError as exc:
            issues=[{"path":".".join(str(v) for v in e["loc"]),"type":e["type"],"message":e["msg"][:120]} for e in exc.errors()[:10]]
            raise ToolCallRejected(json.dumps({"validation_errors":issues})) from exc
        try: return {"ok":True,"result":self.handlers[name](args)}
        except Exception as exc: raise RuntimeError(f"trusted handler failed: {name}") from exc

def build_demo_gate():
    return ArgumentGate({"search":SearchArgs},{"search":demo_search})
