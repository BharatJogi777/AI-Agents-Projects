"""Generate evidence-traceable code change proposals."""
from __future__ import annotations
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Change:
    action: str
    rationale: str
    affected_area: str
    verification: str


@dataclass(frozen=True)
class Proposal:
    goal: str
    changes: tuple[Change, ...]
    assumptions: tuple[str, ...]
    review_gates: tuple[str, ...]


def create_proposal(goal: str, observations: list[str], constraints: list[str] | None = None) -> Proposal:
    if not isinstance(goal, str) or not goal.strip():
        raise ValueError("goal must be non-empty")
    if not isinstance(observations, list) or any(not isinstance(x, str) or not x.strip() for x in observations):
        raise ValueError("observations must contain non-empty strings")
    constraints = [] if constraints is None else constraints
    if not isinstance(constraints, list) or any(not isinstance(x, str) or not x.strip() for x in constraints):
        raise ValueError("constraints must contain non-empty strings")
    changes = tuple(Change(
        action=f"Investigate and address: {item.strip()}",
        rationale=f"Repository observation supplied: {item.strip()}",
        affected_area="Unconfirmed; locate owning module before editing",
        verification="Add a focused regression test and run the relevant test suite",
    ) for item in observations)
    assumptions = ("Observations are accurate but have not been independently verified",) if observations else (
        "No repository observations supplied; discovery is required before proposing concrete edits",
    )
    return Proposal(goal.strip(), changes, tuple(constraints) or assumptions, (
        "Confirm affected interfaces and backward compatibility",
        "Review security and data migration implications",
        "Require human approval before applying or merging changes",
    ))


def to_json(proposal: Proposal) -> str:
    return json.dumps(asdict(proposal), indent=2)


if __name__ == "__main__":
    print(to_json(create_proposal("Improve request validation", ["Validation is duplicated in two handlers"])))
