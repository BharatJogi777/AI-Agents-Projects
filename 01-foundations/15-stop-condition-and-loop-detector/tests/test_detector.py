import threading

import pytest

from app import InvalidAgentState, LoopDetector, StopDecision, evaluate_stop, fingerprint_state


def test_repeated_state_detected_after_configured_repeats():
    detector = LoopDetector(max_repeats=2)
    state = {"tool": "search", "q": "x"}
    assert detector.observe(state) == StopDecision(False, "continue")
    assert detector.observe(state) == StopDecision(False, "continue")
    assert detector.observe({"q": "x", "tool": "search"}) == StopDecision(True, "repeated_state")


def test_state_order_does_not_change_fingerprint():
    assert fingerprint_state({"a": 1, "b": 2}) == fingerprint_state({"b": 2, "a": 1})


def test_json_arrays_are_canonicalized_consistently():
    assert fingerprint_state((1, "x")) == fingerprint_state([1, "x"])


def test_history_is_bounded_and_publicly_observable():
    detector = LoopDetector(max_repeats=2, history_size=3)
    for number in range(10):
        detector.observe({"n": number})
    assert detector.history_size == 3


def test_old_state_ages_out_of_rolling_window():
    detector = LoopDetector(max_repeats=1, history_size=2)
    assert not detector.observe({"n": 1}).stop
    detector.observe({"n": 2})
    detector.observe({"n": 3})
    assert not detector.observe({"n": 1}).stop


def test_reset_clears_state_between_runs():
    detector = LoopDetector(max_repeats=1)
    detector.observe({"step": "same"})
    detector.reset()
    assert detector.history_size == 0
    assert not detector.observe({"step": "same"}).stop


def test_stop_priority_is_deterministic():
    assert evaluate_stop(final_answer=True, cancelled=True, deadline_exceeded=False,
                         step_count=9, max_steps=5).reason == "cancelled"
    assert evaluate_stop(final_answer=True, cancelled=False, deadline_exceeded=True,
                         step_count=9, max_steps=5).reason == "deadline_exceeded"
    assert evaluate_stop(final_answer=True, cancelled=False, deadline_exceeded=False,
                         step_count=9, max_steps=5).reason == "final_answer"
    assert evaluate_stop(final_answer=False, cancelled=False, deadline_exceeded=False,
                         step_count=9, max_steps=5).reason == "step_limit"


def test_detector_stop_is_used_only_after_higher_priority_conditions():
    repeated = StopDecision(True, "repeated_state")
    assert evaluate_stop(final_answer=False, cancelled=False, deadline_exceeded=False,
                         step_count=1, max_steps=5, detector_decision=repeated).reason == "repeated_state"
    assert evaluate_stop(final_answer=True, cancelled=False, deadline_exceeded=False,
                         step_count=1, max_steps=5, detector_decision=repeated).reason == "final_answer"


def test_continue_when_no_condition_is_met():
    assert evaluate_stop(final_answer=False, cancelled=False, deadline_exceeded=False,
                         step_count=1, max_steps=3).reason == "continue"


@pytest.mark.parametrize("state", [
    {"secret": object()},
    {1: "non-string key"},
    {"not_finite": float("nan")},
    {"not_finite": float("inf")},
])
def test_rejects_non_json_or_non_finite_values(state):
    with pytest.raises(InvalidAgentState):
        fingerprint_state(state)


def test_rejects_cycles():
    state = []
    state.append(state)
    with pytest.raises(InvalidAgentState):
        fingerprint_state(state)


def test_rejects_oversized_and_deep_states():
    with pytest.raises(InvalidAgentState, match="byte"):
        fingerprint_state({"data": "x" * 500}, max_bytes=128)
    with pytest.raises(InvalidAgentState, match="nesting"):
        fingerprint_state({"a": {"b": {"c": 1}}}, max_depth=2)


def test_rejects_item_explosion():
    with pytest.raises(InvalidAgentState, match="item"):
        fingerprint_state(list(range(10)), max_items=5)


def test_rejects_invalid_limits_and_bool_as_integer():
    with pytest.raises(ValueError):
        fingerprint_state({}, max_bytes=True)
    with pytest.raises(ValueError):
        LoopDetector(max_repeats=True)
    with pytest.raises(ValueError):
        LoopDetector(max_repeats=2, history_size=2)


def test_stop_policy_rejects_invalid_signal_types():
    with pytest.raises(TypeError):
        evaluate_stop(final_answer=1, cancelled=False, deadline_exceeded=False,
                      step_count=0, max_steps=3)
    with pytest.raises(ValueError):
        evaluate_stop(final_answer=False, cancelled=False, deadline_exceeded=False,
                      step_count=True, max_steps=3)


def test_concurrent_observations_keep_history_bounded():
    detector = LoopDetector(max_repeats=2, history_size=20)
    threads = [
        threading.Thread(target=lambda n=n: [detector.observe({"n": n}) for _ in range(100)])
        for n in range(8)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert detector.history_size == 20
