import threading

import pytest

from app import CircuitBreaker, CircuitOpen, CircuitState


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


def fail(error=ConnectionError("dependency unavailable")):
    raise error


def test_opens_after_failure_threshold_and_rejects_calls():
    clock = Clock()
    breaker = CircuitBreaker(2, 5, clock)
    for _ in range(2):
        with pytest.raises(ConnectionError):
            breaker.call(fail)
    assert breaker.snapshot().state is CircuitState.OPEN
    with pytest.raises(CircuitOpen):
        breaker.call(lambda: "should not run")


def test_half_open_probe_closes_after_success():
    clock = Clock()
    breaker = CircuitBreaker(1, 5, clock)
    with pytest.raises(OSError):
        breaker.call(fail, OSError("offline"))
    clock.advance(5)
    assert breaker.call(lambda: "recovered") == "recovered"
    snapshot = breaker.snapshot()
    assert snapshot.state is CircuitState.CLOSED
    assert snapshot.failures == 0


def test_half_open_failure_reopens_with_new_recovery_window():
    clock = Clock()
    breaker = CircuitBreaker(1, 2, clock)
    with pytest.raises(OSError):
        breaker.call(fail, OSError("offline"))
    clock.advance(2)
    with pytest.raises(OSError):
        breaker.call(fail, OSError("still offline"))
    assert breaker.snapshot().state is CircuitState.OPEN
    assert breaker.snapshot().retry_at == 4


def test_only_one_half_open_probe_is_allowed():
    clock = Clock()
    breaker = CircuitBreaker(1, 1, clock)
    with pytest.raises(OSError):
        breaker.call(fail, OSError())
    clock.advance(1)
    entered = threading.Event()
    release = threading.Event()

    def probe():
        entered.set()
        release.wait(timeout=2)
        return "ok"

    worker = threading.Thread(target=lambda: breaker.call(probe))
    worker.start()
    assert entered.wait(timeout=2)
    with pytest.raises(CircuitOpen):
        breaker.call(lambda: "second probe")
    release.set()
    worker.join(timeout=2)
    assert not worker.is_alive()
    assert breaker.snapshot().state is CircuitState.CLOSED


def test_late_success_from_old_generation_cannot_close_new_open_circuit():
    clock = Clock()
    breaker = CircuitBreaker(1, 3, clock)
    entered = threading.Event()
    release = threading.Event()

    def slow_success():
        entered.set()
        release.wait(timeout=2)
        return "late"

    worker = threading.Thread(target=lambda: breaker.call(slow_success))
    worker.start()
    assert entered.wait(timeout=2)
    with pytest.raises(ConnectionError):
        breaker.call(fail)
    assert breaker.snapshot().state is CircuitState.OPEN
    release.set()
    worker.join(timeout=2)
    assert breaker.snapshot().state is CircuitState.OPEN


def test_cancellation_like_base_exception_releases_half_open_probe():
    clock = Clock()
    breaker = CircuitBreaker(1, 1, clock)
    with pytest.raises(OSError):
        breaker.call(fail, OSError())
    clock.advance(1)

    class Cancelled(BaseException):
        pass

    with pytest.raises(Cancelled):
        breaker.call(fail, Cancelled())
    assert breaker.snapshot().state is CircuitState.HALF_OPEN
    assert breaker.call(lambda: "probe again") == "probe again"


def test_ordinary_failure_increments_counter_but_success_resets_it():
    breaker = CircuitBreaker(3, 5, Clock())
    with pytest.raises(ConnectionError):
        breaker.call(fail)
    assert breaker.snapshot().failures == 1
    breaker.call(lambda: "healthy")
    assert breaker.snapshot().failures == 0


@pytest.mark.parametrize("threshold,recovery", [
    (0, 1), (True, 1), (1001, 1), (1, 0), (1, 3601), (1, float("inf")),
])
def test_invalid_configuration_is_rejected(threshold, recovery):
    with pytest.raises(ValueError):
        CircuitBreaker(threshold, recovery)


def test_operation_must_be_callable():
    breaker = CircuitBreaker()
    with pytest.raises(TypeError):
        breaker.call("not callable")
