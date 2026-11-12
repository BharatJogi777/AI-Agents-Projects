"""Centralized, deterministic stop-condition priority."""
from __future__ import annotations

from .detector import StopDecision


def evaluate_stop(
    *,
    final_answer: bool,
    cancelled: bool,
    deadline_exceeded: bool,
    step_count: int,
    max_steps: int,
    detector_decision: StopDecision | None = None,
) -> StopDecision:
    """Choose one stop reason using a stable priority order.

    Priority: cancellation > deadline > final answer > step limit >
    repeated state > continue.
    """
    for name, value in (
        ("final_answer", final_answer),
        ("cancelled", cancelled),
        ("deadline_exceeded", deadline_exceeded),
    ):
        if type(value) is not bool:
            raise TypeError(f"{name} must be a boolean")
    if type(step_count) is not int or step_count < 0:
        raise ValueError("step_count must be a non-negative integer")
    if type(max_steps) is not int or max_steps < 1:
        raise ValueError("max_steps must be a positive integer")
    if detector_decision is not None and not isinstance(detector_decision, StopDecision):
        raise TypeError("detector_decision must be StopDecision or None")

    if cancelled:
        return StopDecision(True, "cancelled")
    if deadline_exceeded:
        return StopDecision(True, "deadline_exceeded")
    if final_answer:
        return StopDecision(True, "final_answer")
    if step_count >= max_steps:
        return StopDecision(True, "step_limit")
    if detector_decision is not None and detector_decision.stop:
        return StopDecision(True, "repeated_state")
    return StopDecision(False, "continue")
