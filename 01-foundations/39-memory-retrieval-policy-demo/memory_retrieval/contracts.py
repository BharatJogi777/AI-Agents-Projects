from dataclasses import dataclass
@dataclass(frozen=True)
class Memory:
    id:str
    text:str
    confirmed:bool
    confidence:float
    created_at:float
    expires_at:float|None=None
    sensitive:bool=False
@dataclass(frozen=True)
class RankedMemory:
    memory:Memory
    score:float
