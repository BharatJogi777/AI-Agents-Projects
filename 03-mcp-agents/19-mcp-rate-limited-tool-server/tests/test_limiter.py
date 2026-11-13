import pytest
from app.limiter import TokenBucketLimiter

def test_capacity_and_refill():
    now=[0.0]
    limiter=TokenBucketLimiter(capacity=2,refill_per_second=1,clock=lambda:now[0])
    assert limiter.allow("user:tool") and limiter.allow("user:tool")
    assert not limiter.allow("user:tool")
    now[0]+=1
    assert limiter.allow("user:tool")

def test_keys_are_independent():
    limiter=TokenBucketLimiter(capacity=1,refill_per_second=1)
    assert limiter.allow("alice:search") and limiter.allow("bob:search")

@pytest.mark.parametrize("key,cost",[("",1),("u",0),("u",3)])
def test_invalid_input(key,cost):
    with pytest.raises(ValueError):
        TokenBucketLimiter(capacity=2,refill_per_second=1).allow(key,cost=cost)
