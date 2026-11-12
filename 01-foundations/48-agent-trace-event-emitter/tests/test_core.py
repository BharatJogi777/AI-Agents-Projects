from datetime import datetime,timezone
import pytest
from agent_tracing import *
def test_order_timestamp_and_redaction():
 events=[];clock=lambda:datetime(2026,1,1,tzinfo=timezone.utc);t=TraceEmitter("run-1",events.append,clock=clock)
 a=t.emit("started",{"model":"local","api_key":"secret"})
 b=t.emit("completed",{"tokens":12})
 assert [a.sequence,b.sequence]==[1,2] and a.timestamp.tzinfo==timezone.utc
 assert a.attributes["api_key"]=="[REDACTED]"
def test_bounds_and_validation():
 t=TraceEmitter("r",lambda e:None,max_attributes=1,max_value_chars=3)
 assert t.emit("x",{"message":"abcdef"}).attributes["message"]=="abc"
 with pytest.raises(ValueError):t.emit("x",{"a":1,"b":2})
 with pytest.raises(ValueError):t.emit("x"*101)
def test_sink_failure_does_not_reuse_sequence():
 seen=[]
 def sink(e):
  seen.append(e.sequence)
  if e.sequence==1:raise RuntimeError("sink unavailable")
 t=TraceEmitter("r",sink)
 with pytest.raises(RuntimeError):t.emit("event")
 assert t.emit("event").sequence==2 and seen==[1,2]
