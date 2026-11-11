"""Parse fragmented OpenAI-compatible SSE frames into incremental text events."""
import json
from dataclasses import dataclass

@dataclass(frozen=True)
class StreamEvent:
    text:str
    finished:bool=False
    finish_reason:str|None=None

class StreamProtocolError(ValueError): pass

class ChatCompletionStreamParser:
    def __init__(self): self._buffer=""; self._finished=False
    def feed(self,chunk:str)->list[StreamEvent]:
        if self._finished: raise StreamProtocolError("stream already finished")
        if not isinstance(chunk,str): raise TypeError("chunk must be text")
        self._buffer+=chunk; out=[]
        while "\n\n" in self._buffer:
            frame,self._buffer=self._buffer.split("\n\n",1)
            event=self._parse(frame)
            if event is not None:
                out.append(event)
                if event.finished: self._finished=True
        return out
    def close(self)->list[StreamEvent]:
        if not self._buffer.strip(): self._buffer=""; return []
        frame,self._buffer=self._buffer,""
        event=self._parse(frame)
        return [event] if event else []
    def _parse(self,frame):
        data="\n".join(line[5:].lstrip() for line in frame.splitlines() if line.startswith("data:"))
        if not data: return None
        if data=="[DONE]": self._finished=True; return StreamEvent("",True,"stop")
        try: payload=json.loads(data)
        except json.JSONDecodeError as exc: raise StreamProtocolError("invalid SSE JSON") from exc
        try:
            choice=payload["choices"][0]; delta=choice.get("delta",{})
            text=delta.get("content") or ""; reason=choice.get("finish_reason")
            if not isinstance(text,str): raise TypeError()
            return StreamEvent(text,reason is not None,reason)
        except (KeyError,IndexError,TypeError,AttributeError) as exc:
            raise StreamProtocolError("invalid stream event shape") from exc
