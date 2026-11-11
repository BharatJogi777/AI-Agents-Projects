import pytest
from app import RetryPolicy,RetryExhausted,retry


def test_success_after_transient_failures():
    attempts={"n":0}; delays=[]
    def op():
        attempts["n"]+=1
        if attempts["n"]<3: raise ConnectionError("temporary")
        return "ok"
    assert retry(op,RetryPolicy(4,.1,1,0),sleep=delays.append)=="ok"
    assert attempts["n"]==3 and delays==[.1,.2]


def test_exhaustion_preserves_cause():
    def fail(): raise TimeoutError("down")
    with pytest.raises(RetryExhausted) as err:
        retry(fail,RetryPolicy(2,0,0,0),sleep=lambda _:None)
    assert err.value.attempts==2
    assert isinstance(err.value.__cause__,TimeoutError)


def test_non_retryable_exception_propagates_immediately():
    calls=[]
    def fail(): calls.append(1); raise ValueError("bad request")
    with pytest.raises(ValueError):
        retry(fail,RetryPolicy(),retry_if=lambda e:isinstance(e,ConnectionError),sleep=lambda _:None)
    assert len(calls)==1


def test_jitter_is_bounded_and_capped():
    delays=[]
    def fail(): raise OSError()
    with pytest.raises(RetryExhausted):
        retry(fail,RetryPolicy(4,.5,.75,.2),sleep=delays.append,random_value=lambda:1)
    assert delays==[.6,.75,.75]


def test_policy_validation():
    with pytest.raises(ValueError): RetryPolicy(max_attempts=0)
