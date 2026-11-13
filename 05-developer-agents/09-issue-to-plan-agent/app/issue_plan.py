"""Build an implementation plan while preserving issue provenance."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class IssuePlan:
    objective: str
    stated_requirements: tuple[str, ...]
    acceptance_criteria: tuple[str, ...]
    suggested_test_cases: tuple[str, ...]
    risks: tuple[str, ...]
    open_questions: tuple[str, ...]


def create_plan(title: str, body: str) -> IssuePlan:
    if not isinstance(title, str) or not title.strip():
        raise ValueError("title must be non-empty")
    if not isinstance(body, str):
        raise TypeError("body must be text")
    lines = tuple(line.strip(" -*\t") for line in body.splitlines() if line.strip(" -*\t"))
    requirements = tuple(line for line in lines if any(
        marker in line.lower() for marker in ("must ", "should ", "require", "support ", "allow ")
    ))
    criteria = tuple(f"Verify: {item}" for item in requirements)
    if not criteria:
        criteria = ("Confirm the requested behavior against an agreed example",)
    tests = (
        "Add a focused unit test for the primary success path",
        "Cover invalid input and boundary conditions",
        "Verify failure handling and that existing behavior remains unchanged",
    )
    risks = []
    lowered = body.lower()
    if any(word in lowered for word in ("database", "schema", "migration")):
        risks.append("Data compatibility and migration/rollback behavior need review")
    if any(word in lowered for word in ("auth", "permission", "secret", "token")):
        risks.append("Authorization and sensitive-data handling need a security review")
    if any(word in lowered for word in ("async", "concurrent", "parallel", "queue")):
        risks.append("Concurrency, ordering, and retry semantics need explicit tests")
    questions = []
    if not requirements:
        questions.append("What observable behavior and constraints define completion?")
    if not any(word in lowered for word in ("test", "expected", "acceptance")):
        questions.append("What are the expected results and acceptance examples?")
    return IssuePlan(title.strip(), requirements, criteria, tests, tuple(risks), tuple(questions))


def to_json(plan: IssuePlan) -> str:
    return json.dumps(asdict(plan), indent=2)


if __name__ == "__main__":
    print(to_json(create_plan("Add export", "The endpoint must support CSV export.")))
