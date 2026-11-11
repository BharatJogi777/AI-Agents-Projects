from typing import Callable
from .contracts import Entity,EntityExtractionError
class EntityExtractor:
    """Validate extractor candidates against exact source spans before returning them."""
    def __init__(self,extractor:Callable[[str],list[dict]],allowed_kinds:set[str],max_text_chars:int=20000,max_entities:int=500):
        if not allowed_kinds or any(not isinstance(x,str) or not x.strip() for x in allowed_kinds): raise ValueError("allowed_kinds must contain non-empty names")
        if type(max_text_chars) is not int or max_text_chars<1 or type(max_entities) is not int or max_entities<1: raise ValueError("limits must be positive integers")
        if not callable(extractor): raise TypeError("extractor must be callable")
        self.extractor=extractor; self.allowed_kinds=frozenset(allowed_kinds); self.max_text_chars=max_text_chars; self.max_entities=max_entities
    def extract(self,text:str)->list[Entity]:
        if not isinstance(text,str) or not text.strip(): raise ValueError("text cannot be empty")
        if len(text)>self.max_text_chars: raise EntityExtractionError("input exceeds configured length")
        raw=self.extractor(text)
        if not isinstance(raw,list): raise EntityExtractionError("extractor must return a list")
        if len(raw)>self.max_entities: raise EntityExtractionError("extractor returned too many entities")
        result=[]; seen=set()
        for item in raw:
            if not isinstance(item,dict): raise EntityExtractionError("entity must be an object")
            kind,value,evidence=(item.get(key) for key in ("kind","value","evidence"))
            if not isinstance(kind,str) or kind not in self.allowed_kinds or not all(isinstance(x,str) and x.strip() for x in (value,evidence)):
                raise EntityExtractionError("invalid entity fields")
            start=text.find(evidence)
            if start<0 or value not in evidence: raise EntityExtractionError("entity evidence is not grounded in source text")
            end=start+len(evidence); key=(kind,value,start,end)
            if key in seen: continue
            seen.add(key); result.append(Entity(kind,value,evidence,start,end))
        return result
