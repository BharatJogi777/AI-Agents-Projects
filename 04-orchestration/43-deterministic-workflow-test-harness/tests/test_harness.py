from app.harness import DeterministicHarness

def test_retry_uses_controlled_clock():
    harness = DeterministicHarness(); calls = 0
    def flaky():
        nonlocal calls
        calls += 1
        if calls < 3: raise RuntimeError("temporary")
        return "ok"
    result = harness.run_step("fetch", flaky, max_attempts=3, retry_delay=2)
    assert (result.value, result.attempts, result.error) == ("ok", 3, None)
    assert harness.now == 4
    assert harness.trace == [("fetch", 0), ("fetch", 2), ("fetch", 4)]

def test_invalid_parameters():
    import pytest
    with pytest.raises(ValueError): DeterministicHarness().advance(-1)
