import pytest
from app import (LoopConfig,StepResult,run_bounded_loop,AgentStepLimitExceeded,
                 AgentToolLimitExceeded)


def test_returns_final_report():
    report=run_bounded_loop(lambda n: StepResult(final=n==2,tool_calls=1,value=n))
    assert (report.steps,report.tool_calls,report.value,report.stopped_reason)==(2,2,2,"final_answer")


def test_step_limit_is_enforced():
    with pytest.raises(AgentStepLimitExceeded):
        run_bounded_loop(lambda n: StepResult(value=n),LoopConfig(max_steps=2))


def test_tool_call_budget_is_enforced_before_overshoot():
    with pytest.raises(AgentToolLimitExceeded):
        run_bounded_loop(lambda n: StepResult(tool_calls=2),LoopConfig(max_tool_calls=3))


def test_consecutive_error_threshold_stops():
    report=run_bounded_loop(lambda n: StepResult(errors=1,value=n),
                            LoopConfig(max_consecutive_errors=2))
    assert report.stopped_reason=="consecutive_error_limit"
    assert report.steps==2


def test_success_resets_consecutive_error_count():
    def step(n): return StepResult(errors=1 if n in (1,3,4) else 0,final=n==4)
    report=run_bounded_loop(step,LoopConfig(max_consecutive_errors=2))
    assert report.stopped_reason=="consecutive_error_limit"
    assert report.steps==4


def test_invalid_config_and_result_rejected():
    with pytest.raises(ValueError): LoopConfig(max_steps=0)
    with pytest.raises(TypeError): run_bounded_loop(lambda _: {})
