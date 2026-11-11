"""Extract entities through an injected model function and validate evidence grounding."""
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class Entity:
    kind:str
    value:str
    evidence:str
    start:int
    end:int

class EntityExtractionError(ValueError): pass

class EntityExtractor:
    def __init__(self,extractor:Callable[[str],list[dict]],allowed_kinds:set[str],max_text_chars:int=20000):
        if not allowed_kinds or max_text_chars<1: raise ValueError("invalid extractor configuration")
        self.extractor=extractor; self.allowed_kinds=set(allowed_kinds); self.max_text_chars=max_text_chars
    def extract(self,text:str)->list[Entity]:
        if not isinstance(text,str) or not text.strip(): raise ValueError("text cannot be empty")
        if len(text)>self.max_text_chars: raise EntityExtractionError("input exceeds configured length")
        raw=self.extractor(text)
        if not isinstance(raw,list): raise EntityExtractionError("extractor must return a list")
        result=[]; seen=set()
        for item in raw:
            if not isinstance(item,dict): raise EntityExtractionError("entity must be an object")
            kind,value,evidence=(item.get(k) for k in ("kind","value","evidence"))
            if kind not in self.allowed_kinds or not all(isinstance(x,str) and x for x in (value,evidence)):
                raise EntityExtractionError("invalid entity fields")
            start=text.find(evidence)
            if start<0 or value not in evidence: raise EntityExtractionError("entity evidence is not grounded in source text")
            key=(kind,value,start)
            if key in seen: continue
            seen.add(key); result.append(Entity(kind,value,evidence,start,start+len(evidence)))
        return result
