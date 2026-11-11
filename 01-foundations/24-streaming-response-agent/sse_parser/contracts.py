from dataclasses import dataclass
class StreamProtocolError(ValueError): pass
@dataclass(frozen=True)
class StreamEvent:
    text:str
    finished:bool=False
    finish_reason:str|None=None
