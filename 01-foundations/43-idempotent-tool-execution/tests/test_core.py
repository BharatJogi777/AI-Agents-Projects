from concurrent.futures import ThreadPoolExecutor
import pytest
from idempotent_tools import *
def test_canonical_payload_replay():
 e=IdempotentExecutor();calls=[]
 a=e.execute("k",{"b":2,"a":1},lambda p:calls.append(1) or "result")
 b=e.execute("k",{"a":1,"b":2},lambda p:"other")
 assert a==b=="result" and calls==[1]
def test_conflict_and_non_json():
 e=IdempotentExecutor();e.execute("k",{"x":1},lambda p:1)
 with pytest.raises(IdempotencyConflict):e.execute("k",{"x":2},lambda p:2)
 with pytest.raises(ValueError):fingerprint({"x":float("nan")})
def test_failed_handler_allows_retry():
 e=IdempotentExecutor()
 with pytest.raises(IdempotencyExecutionError):e.execute("k",{},lambda p:1/0)
 assert e.execute("k",{},lambda p:"ok")=="ok"
def test_concurrent_replay_executes_once():
 e=IdempotentExecutor();calls=[]
 def handler(p):calls.append(1);return "done"
 with ThreadPoolExecutor(8) as pool:r=list(pool.map(lambda _:e.execute("same",{"a":1},handler),range(20)))
 assert r==["done"]*20 and len(calls)==1
