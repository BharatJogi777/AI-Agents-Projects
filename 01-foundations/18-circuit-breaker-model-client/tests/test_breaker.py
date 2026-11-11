import pytest
from app import CircuitBreaker,CircuitOpen,CircuitState


class Clock:
    def __init__(self): self.now=0.0
    def __call__(self): return self.now
    def advance(self,seconds): self.now+=seconds


def test_opens_after_failure_threshold():
    clock=Clock(); breaker=CircuitBreaker(2,5,clock)
    for _ in range(2):
        with pytest.raises(ConnectionError): breaker.call(lambda:(_ for _ in ()).throw(ConnectionError()))
    assert breaker.snapshot().state is CircuitState.OPEN
    with pytest.raises(CircuitOpen): breaker.call(lambda:"ok")


def test_half_open_probe_closes_after_success():
    clock=Clock(); b=CircuitBreaker(1,5,clock)
    with pytest.raises(OSError): b.call(lambda:(_ for _ in ()).throw(OSError()))
    clock.advance(5)
    assert b.call(lambda:"recovered")=="recovered"
    assert b.snapshot().state is CircuitState.CLOSED


def test_half_open_failure_reopens():
    clock=Clock(); b=CircuitBreaker(1,2,clock)
    with pytest.raises(OSError): b.call(lambda:(_ for _ in ()).throw(OSError()))
    clock.advance(2)
    with pytest.raises(OSError): b.call(lambda:(_ for _ in ()).throw(OSError()))
    assert b.snapshot().state is CircuitState.OPEN


def test_only_one_half_open_probe_allowed():
    clock=Clock(); b=CircuitBreaker(1,1,clock)
    with pytest.raises(OSError): b.call(lambda:(_ for _ in ()).throw(OSError()))
    clock.advance(1)
    b.before_call()
    with pytest.raises(CircuitOpen): b.before_call()
    b.record_success()


def test_configuration_validation():
    with pytest.raises(ValueError): CircuitBreaker(0,1)
