import pytest
from conversation_memory import *
def test_complete_turn_eviction_preserves_system():
 m=ShortTermMemory(4)
 for item in [Message("system","rules"),Message("user","one","1"),Message("assistant","reply","1"),Message("user","two","2"),Message("assistant","reply","2")]:m.append(item)
 assert [x.turn_id for x in m.snapshot()]==[None,"2","2"]
def test_bad_message_and_clear():
 m=ShortTermMemory()
 with pytest.raises(ValueError):m.append(Message("tool","x","1"))
 m.append(Message("user","hi","1"));m.clear();assert m.snapshot()==()
