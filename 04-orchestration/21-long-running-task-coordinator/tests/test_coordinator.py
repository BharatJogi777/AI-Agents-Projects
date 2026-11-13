import pytest
from app.coordinator import TaskCoordinator, Status

def test_claim_heartbeat_and_finish():
    c=TaskCoordinator(); c.submit("a"); t=c.claim("a", now=10)
    assert t.status == Status.RUNNING and t.lease_until == 70
    c.heartbeat("a", now=20); assert t.lease_until == 80
    c.finish("a","ok"); assert t.status == Status.SUCCEEDED

def test_retry_budget():
    c=TaskCoordinator(max_attempts=2); c.submit("a")
    c.claim("a"); c.fail("a","temporary"); c.claim("a"); c.fail("a","again")
    with pytest.raises(RuntimeError): c.claim("a")

def test_cancel_prevents_claim():
    c=TaskCoordinator(); c.submit("a"); c.cancel("a")
    with pytest.raises(RuntimeError): c.claim("a")
