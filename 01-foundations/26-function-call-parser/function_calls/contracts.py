from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FunctionCall:
    call_id:str
    name:str
    arguments:dict[str,Any]
class FunctionCallError(ValueError): pass
