import json
from .contracts import StreamEvent,StreamProtocolError

class ChatCompletionStreamParser:
    """Incremental SSE parser with bounded frames and terminal-state enforcement."""
    def __init__(self,max_frame_chars:int=1_000_000):
        if not 128<=max_frame_chars<=10_000_000: raise ValueError("max_frame_chars must be 128..10000000")
        self.max_frame_chars=max_frame_chars; self._buffer=""; self._finished=False
    @property
    def finished(self): return self._finished
    def feed(self,chunk:str)->list[StreamEvent]:
        if self._finished: raise StreamProtocolError("stream already finished")
        if not isinstance(chunk,str): raise TypeError("chunk must be text")
        self._buffer+=chunk
        if len(self._buffer)>self.max_frame_chars: raise StreamProtocolError("SSE frame buffer limit exceeded")
        output=[]
        while True:
            # SSE permits CRLF or LF line endings; normalize complete delimiters.
            index=self._buffer.find("\n\n")
            crlf=self._buffer.find("\r\n\r\n")
            if index<0 and crlf<0: break
            if crlf>=0 and (index<0 or crlf<index):
                frame,self._buffer=self._buffer[:crlf],self._buffer[crlf+4:]
            else:
                frame,self._buffer=self._buffer[:index],self._buffer[index+2:]
            event=self._parse(frame)
            if event is not None: output.append(event)
            if self._finished:
                if self._buffer.strip(): raise StreamProtocolError("data received after terminal event")
                self._buffer=""; break
        return output
    def close(self)->list[StreamEvent]:
        if self._finished:
            if self._buffer.strip(): raise StreamProtocolError("data received after terminal event")
            self._buffer=""; return []
        if not self._buffer.strip(): self._buffer=""; return []
        frame,self._buffer=self._buffer,""
        event=self._parse(frame)
        return [event] if event else []
    def _parse(self,frame:str)->StreamEvent|None:
        data_lines=[]
        for line in frame.replace("\r\n","\n").split("\n"):
            if not line or line.startswith(":"): continue
            if line.startswith("data:"): data_lines.append(line[5:].lstrip(" "))
        if not data_lines: return None
        data="\n".join(data_lines)
        if data=="[DONE]":
            self._finished=True; return StreamEvent("",True,"stop")
        try: payload=json.loads(data)
        except json.JSONDecodeError as exc: raise StreamProtocolError("invalid SSE JSON") from exc
        try:
            choices=payload["choices"]
            if not isinstance(choices,list) or not choices: raise ValueError()
            choice=choices[0]; delta=choice.get("delta",{})
            if not isinstance(delta,dict): raise ValueError()
            content=delta.get("content") or ""; reason=choice.get("finish_reason")
            if not isinstance(content,str) or (reason is not None and not isinstance(reason,str)): raise ValueError()
            finished=reason is not None
            if finished: self._finished=True
            return StreamEvent(content,finished,reason)
        except (KeyError,IndexError,TypeError,ValueError,AttributeError) as exc:
            raise StreamProtocolError("invalid stream event shape") from exc
