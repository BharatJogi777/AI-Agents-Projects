import pytest
from app import *
def test_ttl_and_isolation():
 now=[10.];s=SessionMemoryStore(clock=lambda:now[0]);s.put("a","k","v",5)
 assert s.get("a","k")=="v" and s.get("b","k") is None
 now[0]=15;assert s.get("a","k") is None
def test_capacity_delete():
 s=SessionMemoryStore(1,clock=lambda:0);s.put("a","x","1",5)
 with pytest.raises(OverflowError):s.put("b","x","2",5)
 assert s.delete_session("a")==1
