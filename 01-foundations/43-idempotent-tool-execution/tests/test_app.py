import pytest
from app import *
def test_replay():
 e=IdempotentExecutor(); calls=[]; f=lambda p:calls.append(p["v"]) or "ok"
 assert e.execute("k",{"v":1},f)==e.execute("k",{"v":1},f)=="ok" and calls==[1]
def test_conflict_and_key_validation():
 e=IdempotentExecutor(); e.execute("k",{"v":1},lambda p:1)
 with pytest.raises(IdempotencyConflict): e.execute("k",{"v":2},lambda p:2)
 with pytest.raises(ValueError): e.execute("",{},lambda p:None)
