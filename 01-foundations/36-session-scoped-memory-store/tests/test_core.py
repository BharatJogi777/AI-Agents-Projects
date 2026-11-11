import pytest
from session_memory import SessionMemoryStore
def test_ttl_isolation_and_capacity():
 now=[10.];s=SessionMemoryStore(1,clock=lambda:now[0]);s.put("a","k","v",5)
 assert s.get("a","k")=="v" and s.get("b","k") is None
 with pytest.raises(OverflowError):s.put("b","k","v",5)
 now[0]=15;assert s.get("a","k") is None;s.put("b","k","v",5)
def test_invalid_ttl():
 with pytest.raises(ValueError):SessionMemoryStore().put("s","k","v",float("nan"))
