from dataclasses import dataclass
@dataclass(frozen=True)
class Route:
    name:str
    confidence:float
    source:str
