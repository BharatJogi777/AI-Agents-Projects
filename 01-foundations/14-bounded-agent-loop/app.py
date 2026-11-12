"""Backward-compatible facade; use agent_loop for new code."""
from agent_loop import (
    AgentErrorLimitExceeded,
    AgentLoopError,
    AgentStepLimitExceeded,
    AgentToolLimitExceeded,
    LoopConfig,
    LoopReport,
    StepResult,
    StepSummary,
    run_bounded_loop,
)

__all__ = [
    "AgentErrorLimitExceeded",
    "AgentLoopError",
    "AgentStepLimitExceeded",
    "AgentToolLimitExceeded",
    "LoopConfig",
    "LoopReport",
    "StepResult",
    "StepSummary",
    "run_bounded_loop",
]
