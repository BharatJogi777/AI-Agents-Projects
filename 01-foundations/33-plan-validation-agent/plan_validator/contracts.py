from dataclasses import dataclass
@dataclass(frozen=True)
class Step:
    id:str
    action:str
    depends_on:tuple[str,...]=()
    risk:str="low"
@dataclass(frozen=True)
class Validation:
    valid:bool
    errors:tuple[str,...]
    topological_order:tuple[str,...]=()
