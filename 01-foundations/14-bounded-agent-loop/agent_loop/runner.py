from __future__ import annotations

from collections.abc import Callable
from typing import TypeAlias

from .contracts import (
    AgentErrorLimitExceeded,
    AgentStepLimitExceeded,
    AgentToolLimitExceeded,
    LoopConfig,
    LoopReport,
    StepResult,
    StepSummary,
)

StepCallback: TypeAlias = Callable[[int], StepResult]


def run_bounded_loop(
    step: StepCallback,
    config: LoopConfig | None = None,
) -> LoopReport:
    """Run an agent's single-iteration callback under independent budgets.

    The callback is responsible for one model interaction and any tool
    dispatches it performs. It must report actual tool-call and error counts.
    Provider/network exceptions intentionally propagate; this controller
    does not silently retry failed infrastructure calls.
    """
    if not callable(step):
        raise TypeError("step must be callable")

    active_config = config or LoopConfig()
    total_calls = 0
    total_errors = 0
    consecutive_errors = 0
    last_value = None
    history: list[StepSummary] = []

    for index in range(1, active_config.max_steps + 1):
        result = step(index)
        if not isinstance(result, StepResult):
            raise TypeError("step callback must return StepResult")

        if result.tool_calls > active_config.max_tool_calls_per_step:
            raise AgentToolLimitExceeded(
                f"step {index} attempted {result.tool_calls} tool calls; "
                f"per-step limit is {active_config.max_tool_calls_per_step}"
            )
        if total_calls + result.tool_calls > active_config.max_tool_calls:
            raise AgentToolLimitExceeded(
                f"total tool-call budget would be exceeded at step {index}"
            )

        total_calls += result.tool_calls
        total_errors += result.errors
        consecutive_errors = (
            consecutive_errors + result.errors if result.errors else 0
        )
        last_value = result.value
        history.append(
            StepSummary(
                index=index,
                tool_calls=result.tool_calls,
                errors=result.errors,
                final=result.final,
            )
        )

        if total_errors >= active_config.max_total_errors:
            return LoopReport(
                last_value, index, total_calls, total_errors,
                consecutive_errors, "total_error_limit", tuple(history)
            )

        if consecutive_errors >= active_config.max_consecutive_errors:
            return LoopReport(
                last_value, index, total_calls, total_errors,
                consecutive_errors, "consecutive_error_limit", tuple(history)
            )

        if result.final:
            return LoopReport(
                last_value, index, total_calls, total_errors,
                consecutive_errors, "final_answer", tuple(history)
            )

    raise AgentStepLimitExceeded(
        f"agent did not finish within {active_config.max_steps} steps"
    )
