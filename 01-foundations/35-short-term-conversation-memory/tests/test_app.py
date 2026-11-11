import pytest
from app import *
def test_turn_eviction():
 m=ShortTermMemory(4)
 for x in [Message("system","rules"),Message("user","one","1"),Message("assistant","reply","1"),Message("user","two","2"),Message("assistant","reply","2")]:m.append(x)
 assert [x.turn_id for x in m.snapshot()]==[None,"2","2"]
def test_bad_role():
 with pytest.raises(ValueError):ShortTermMemory().append(Message("tool","x","1"))
def test_clear():
 m=ShortTermMemory();m.append(Message("user","hi","1"));m.clear();assert not m.snapshot()
