from dataclasses import dataclass
@dataclass(frozen=True)
class Entry:
    value:str
    expires_at:float
    created_at:float
