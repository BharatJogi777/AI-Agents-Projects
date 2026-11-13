import pytest

from app import RetryExhausted, RetryPolicy, retry


def test_success_after_transient_failures():
    attempts, delays = {"n": 0}, []
    def operation():
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise ConnectionError("temporary")
        return "ok"
    result = retry(operation, RetryPolicy(4, .1, 1, jitter_ratio=0), idempotent=True, sleep=delays.append)
    assert result == "ok"
    assert attempts["n"] == 3
    assert delays == [.1, .2]


def test_exhaustion_preserves_cause_and_metadata():
    def fail():
        raise TimeoutError("down")
    with pytest.raises(RetryExhausted) as caught:
        retry(fail, RetryPolicy(2, 0, 0, jitter_ratio=0), idempotent=True, sleep=lambda _: None)
    assert caught.value.attempts == 2
    assert isinstance(caught.value.last_error, TimeoutError)
    assert isinstance(caught.value.__cause__, TimeoutError)


def test_non_idempotent_operation_is_never_retried():
    calls = []
    def fail():
        calls.append(1)
        raise ConnectionError("maybe committed")
    with pytest.raises(ConnectionError):
        retry(fail, idempotent=False, sleep=lambda _: None)
    assert len(calls) == 1


def test_only_known_transient_errors_retry_by_default():
    calls = []
    def fail():
        calls.append(1)
        raise OSError("not classified")
    with pytest.raises(OSError):
        retry(fail, idempotent=True, sleep=lambda _: None)
    assert len(calls) == 1


def test_custom_classifier_controls_retry():
    calls = []
    def fail():
        calls.append(1)
        if len(calls) == 1:
            raise OSError("temporary")
        return "done"
    assert retry(fail, idempotent=True, retry_if=lambda e: isinstance(e, OSError), sleep=lambda _: None) == "done"
    assert len(calls) == 2


def test_jitter_is_bounded_and_delay_is_capped():
    delays = []
    def fail():
        raise ConnectionError()
    with pytest.raises(RetryExhausted):
        retry(fail, RetryPolicy(4, .5, .75, jitter_ratio=.2), idempotent=True,
              sleep=delays.append, random_value=lambda: 1)
    assert delays == [.6, .75, .75]


def test_retry_after_is_respected_but_capped():
    delays, calls = [], []
    def fail():
        calls.append(1)
        if len(calls) == 1:
            raise ConnectionError()
        return "ok"
    assert retry(fail, RetryPolicy(3, .1, .5, jitter_ratio=0), idempotent=True,
                 retry_after=lambda _: .4, sleep=delays.append) == "ok"
    assert delays == [.4]


def test_elapsed_budget_prevents_sleep_that_would_exceed_deadline():
    now = [10.0]
    def clock():
        return now[0]
    def sleep(seconds):
        now[0] += seconds
    calls = []
    def fail():
        calls.append(1)
        raise ConnectionError()
    with pytest.raises(RetryExhausted):
        retry(fail, RetryPolicy(5, .4, 1, jitter_ratio=0, max_elapsed=.5),
              idempotent=True, sleep=sleep, clock=clock)
    assert len(calls) == 1


@pytest.mark.parametrize("kwargs", [
    {"max_attempts": 0}, {"max_attempts": True}, {"base_delay": -1},
    {"max_delay": 301}, {"multiplier": .5}, {"jitter_ratio": 1.1},
    {"max_elapsed": 0}, {"max_elapsed": float("inf")},
])
def test_policy_rejects_invalid_configuration(kwargs):
    with pytest.raises(ValueError):
        RetryPolicy(**kwargs)


def test_random_source_is_validated():
    with pytest.raises(ValueError):
        retry(lambda: (_ for _ in ()).throw(ConnectionError()), idempotent=True,
              random_value=lambda: 2, sleep=lambda _: None)


def test_cancellation_like_base_exception_is_not_intercepted():
    class Stop(BaseException):
        pass
    calls = []
    def operation():
        calls.append(1)
        raise Stop()
    with pytest.raises(Stop):
        retry(operation, idempotent=True, sleep=lambda _: None)
    assert len(calls) == 1
