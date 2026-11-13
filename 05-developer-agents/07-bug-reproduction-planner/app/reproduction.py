"""Create conservative reproduction plans from issue text."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Iterable


@dataclass(frozen=True)
class ReproductionPlan:
    summary: str
    reported_environment: tuple[str, ...]
    reported_symptoms: tuple[str, ...]
    reproduction_steps: tuple[str, ...]
    missing_information: tuple[str, ...]
    proposed_experiments: tuple[str, ...]


ENVIRONMENT_MARKERS = ("python ", "python=", "node ", "node=", "ubuntu", "macos", "windows", "docker", "kubernetes", "postgres", "chrome")
SYMPTOM_MARKERS = ("error", "exception", "traceback", "timeout", "crash", "fails", "failed", "unexpected", "hang")


def _sentences(text: str) -> list[str]:
    return [part.strip(" \t-*") for part in text.replace("\r", "").splitlines() if part.strip(" \t-*")]


def build_plan(report: str, existing_steps: Iterable[str] = ()) -> ReproductionPlan:
    if not isinstance(report, str) or not report.strip():
        raise ValueError("report must be a non-empty string")
    lines = _sentences(report)
    env = tuple(line for line in lines if any(marker in line.lower() for marker in ENVIRONMENT_MARKERS))
    symptoms = tuple(line for line in lines if any(marker in line.lower() for marker in SYMPTOM_MARKERS))
    steps = tuple(step.strip() for step in existing_steps if isinstance(step, str) and step.strip())
    missing = []
    if not env:
        missing.append("Exact runtime, operating system, and dependency versions")
    if not steps:
        missing.append("Minimal sequence of actions that triggers the issue")
    if not symptoms:
        missing.append("Expected versus actual result, including exact error output")
    experiments = (
        "Re-run the minimal steps once with debug logging enabled and timestamps",
        "Repeat with the smallest supported input to isolate boundary conditions",
        "Compare against the last known working version or configuration",
    )
    summary = next((line for line in lines if line), "Bug report")
    return ReproductionPlan(summary[:200], env, symptoms, steps, tuple(missing), experiments)


def to_json(plan: ReproductionPlan) -> str:
    return json.dumps(asdict(plan), indent=2)


if __name__ == "__main__":
    print(to_json(build_plan("The API fails with a timeout on Python 3.12\nSteps: start server")))
