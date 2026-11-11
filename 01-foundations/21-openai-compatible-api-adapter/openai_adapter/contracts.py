from dataclasses import dataclass,field

@dataclass(frozen=True)
class Message:
    role:str
    content:str
    def __post_init__(self):
        if self.role not in {"system","user","assistant"}: raise ValueError("unsupported role")
        if not isinstance(self.content,str): raise TypeError("content must be text")
        if len(self.content.encode("utf-8"))>1_000_000: raise ValueError("message exceeds 1 MB")

@dataclass(frozen=True)
class Request:
    model:str
    messages:tuple[Message,...]
    temperature:float=0.0
    max_tokens:int=512
    def __post_init__(self):
        if not isinstance(self.model,str) or not self.model.strip() or not self.messages: raise ValueError("model and messages required")
        if any(not isinstance(m,Message) for m in self.messages): raise TypeError("messages must contain Message values")
        if not 0<=self.temperature<=2 or type(self.max_tokens) is not int or not 1<=self.max_tokens<=32768: raise ValueError("invalid generation limits")

@dataclass(frozen=True)
class Response:
    content:str
    model:str
    finish_reason:str|None=None
    usage:dict[str,int]=field(default_factory=dict)
