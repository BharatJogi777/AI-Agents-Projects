from dataclasses import dataclass
class EntityExtractionError(ValueError): pass
@dataclass(frozen=True)
class Entity:
    kind:str
    value:str
    evidence:str
    start:int
    end:int
