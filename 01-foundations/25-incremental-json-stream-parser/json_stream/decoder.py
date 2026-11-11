import json
from typing import Any
from .contracts import IncrementalJSONError

class IncrementalJSONDecoder:
    """Decode concatenated JSON values from arbitrary text chunks."""
    def __init__(self,max_buffer_chars:int=1_000_000):
        if type(max_buffer_chars) is not int or max_buffer_chars<2: raise ValueError("max_buffer_chars must be >= 2")
        self.max_buffer_chars=max_buffer_chars; self._buffer=""; self._decoder=json.JSONDecoder()
    @property
    def buffered_chars(self)->int: return len(self._buffer)
    def feed(self,chunk:str)->list[Any]:
        if not isinstance(chunk,str): raise TypeError("chunk must be text")
        if len(self._buffer)+len(chunk)>self.max_buffer_chars: raise IncrementalJSONError("JSON stream buffer limit exceeded")
        self._buffer+=chunk; values=[]
        while self._buffer.strip():
            leading=len(self._buffer)-len(self._buffer.lstrip())
            candidate=self._buffer[leading:]
            try: value,end=self._decoder.raw_decode(candidate)
            except json.JSONDecodeError: break
            values.append(value); self._buffer=candidate[end:]
        return values
    def finish(self)->list[Any]:
        candidate=self._buffer.lstrip()
        if not candidate: self._buffer=""; return []
        try: value,end=self._decoder.raw_decode(candidate)
        except json.JSONDecodeError as exc: raise IncrementalJSONError("stream ended with incomplete or invalid JSON") from exc
        if candidate[end:].strip(): raise IncrementalJSONError("trailing non-JSON data")
        self._buffer=""; return [value]
    def reset(self)->None: self._buffer=""
