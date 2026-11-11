from dataclasses import dataclass
@dataclass(frozen=True)
class Message:
    role:str
    content:str
    turn_id:str|None=None
