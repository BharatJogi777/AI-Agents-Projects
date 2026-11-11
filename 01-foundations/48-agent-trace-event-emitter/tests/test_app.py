import pytest
from app import *
def test_order_redaction_and_bound():
 events=[]; t=TraceEmitter("r",events.append); a=t.emit("start",{"api_key":"secret"}); b=t.emit("end",{"text":"x"*600})
 assert (a.sequence,b.sequence)==(1,2) and a.attributes["api_key"]=="[REDACTED]" and len(b.attributes["text"])==500
def test_attribute_limit():
 t=TraceEmitter("r",lambda e:None,max_attributes=1)
 with pytest.raises(ValueError): t.emit("x",{"a":1,"b":2})
