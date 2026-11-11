from dataclasses import dataclass
from typing import Any,Callable,Type
from pydantic import BaseModel,ValidationError

class ToolRegistrationError(ValueError): pass
class ToolExecutionError(RuntimeError): pass

@dataclass(frozen=True)
class ToolSpec:
    name:str
    description:str
    args_model:Type[BaseModel]
    handler:Callable[[BaseModel],Any]
    def provider_schema(self):
        return {"type":"function","function":{"name":self.name,"description":self.description,"parameters":self.args_model.model_json_schema()}}

class ToolRegistry:
    def __init__(self): self._tools={}
    def register(self,name,description,args_model,handler):
        if not name or not name.replace("_","").isalnum(): raise ToolRegistrationError("invalid tool name")
        if name in self._tools: raise ToolRegistrationError(f"duplicate tool: {name}")
        if not isinstance(description,str) or not description.strip(): raise ToolRegistrationError("description required")
        if not isinstance(args_model,type) or not issubclass(args_model,BaseModel): raise ToolRegistrationError("Pydantic model required")
        if not callable(handler): raise ToolRegistrationError("callable handler required")
        self._tools[name]=ToolSpec(name,description,args_model,handler)
    def provider_schemas(self): return [x.provider_schema() for x in self._tools.values()]
    def names(self): return tuple(self._tools)
    def execute(self,name,raw):
        spec=self._tools.get(name)
        if spec is None: raise ToolExecutionError(f"unknown tool: {name}")
        try: args=spec.args_model.model_validate(raw)
        except ValidationError as exc: raise ToolExecutionError(f"invalid arguments for {name}") from exc
        try: return spec.handler(args)
        except Exception as exc: raise ToolExecutionError(f"tool handler failed: {name}") from exc
