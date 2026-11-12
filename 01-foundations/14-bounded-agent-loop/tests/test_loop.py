import pytest

from app import (
    AgentErrorLimitExceeded,
    AgentStepLimitExceeded,
    AgentToolLimitExceeded,
    LoopConfig,
    StepResult,
    run_bounded_loop,
)


def test_returns_final_report_with_per_step_audit_summary():
    report = run_bounded_loop(
        lambda n: StepResult(final=n == 2, tool_calls=1, value={"step": n})
    )
    assert report.steps == 2
    assert report.tool_calls == 2
    assert report.value == {"step": 2}
    assert report.stopped_reason == "final_answer"
    assert [(item.index, item.tool_calls) for item in report.history] == [(1, 1), (2, 1)]


def test_step_limit_is_enforced():
    with pytest.raises(AgentStepLimitExceeded):
        run_bounded_loop(lambda n: StepResult(value=n), LoopConfig(max_steps=2))


def test_total_tool_call_budget_is_enforced_before_overshoot():
    with pytest.raises(AgentToolLimitExceeded, match="total"):
        run_bounded_loop(
            lambda n: StepResult(tool_calls=2),
            LoopConfig(max_tool_calls=3, max_tool_calls_per_step=2),
        )


def test_per_step_tool_call_limit_is_enforced():
    with pytest.raises(AgentToolLimitExceeded, match="per-step"):
        run_bounded_loop(
            lambda _: StepResult(tool_calls=3),
            LoopConfig(max_tool_calls=10, max_tool_calls_per_step=2),
        )


def test_zero_tool_budget_allows_no_tool_calls():
    report = run_bounded_loop(
        lambda _: StepResult(final=True),
        LoopConfig(max_tool_calls=0, max_tool_calls_per_step=0),
    )
    assert report.tool_calls == 0


def test_consecutive_error_threshold_stops():
    report = run_bounded_loop(
        lambda n: StepResult(errors=1, value=n),
        LoopConfig(max_consecutive_errors=2),
    )
    assert report.stopped_reason == "consecutive_error_limit"
    assert report.steps == 2


def test_success_resets_consecutive_error_count():
    def step(n):
        return StepResult(errors=1 if n in (1, 3, 4) else 0, final=n == 5)

    report = run_bounded_loop(step, LoopConfig(max_consecutive_errors=2))
    assert report.stopped_reason == "consecutive_error_limit"
    assert report.steps == 4


def test_total_error_budget_is_independent_of_consecutive_errors():
    report = run_bounded_loop(
        lambda n: StepResult(errors=1, value=n),
        LoopConfig(max_consecutive_errors=3, max_total_errors=2),
    )
    assert report.stopped_reason == "total_error_limit"
    assert report.errors == 2
    assert report.steps == 2


def test_step_result_rejects_boolean_counters():
    with pytest.raises(TypeError, match="integer"):
        StepResult(tool_calls=True)
    with pytest.raises(TypeError, match="integer"):
        StepResult(errors=False)


def test_step_result_rejects_negative_counters_and_non_boolean_final():
    with pytest.raises(ValueError):
        StepResult(tool_calls=-1)
    with pytest.raises(ValueError):
        StepResult(errors=-1)
    with pytest.raises(TypeError, match="boolean"):
        StepResult(final=1)


def test_invalid_config_values_are_rejected():
    for kwargs in (
        {"max_steps": 0},
        {"max_steps": True},
        {"max_tool_calls": -1},
        {"max_tool_calls_per_step": 101},
        {"max_consecutive_errors": 0},
        {"max_total_errors": 0},
    ):
        with pytest.raises(ValueError):
            LoopConfig(**kwargs)


def test_callback_contract_is_checked():
    with pytest.raises(TypeError, match="callable"):
        run_bounded_loop(None)
    with pytest.raises(TypeError, match="StepResult"):
        run_bounded_loop(lambda _: {"final": True})


def test_callback_exception_is_not_silently_retried():
    calls = 0

    def step(_):
        nonlocal calls
        calls += 1
        raise TimeoutError("provider timeout")

    with pytest.raises(TimeoutError):
        run_bounded_loop(step)
    assert calls == 1


def test_final_result_stops_before_another_iteration():
    calls = []
    report = run_bounded_loop(
        lambda n: (calls.append(n) or StepResult(final=True, value="done"))
    )
    assert calls == [1]
    assert report.value == "done"
