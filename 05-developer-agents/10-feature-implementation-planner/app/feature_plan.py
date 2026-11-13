"""Generate phased feature plans from explicitly supplied requirements."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class FeaturePlan:
    feature: str
    scope: tuple[str, ...]
    phases: tuple[tuple[str, tuple[str, ...]], ...]
    quality_gates: tuple[str, ...]
    rollout_checks: tuple[str, ...]
    unresolved_constraints: tuple[str, ...]


def plan_feature(feature: str, requirements: list[str], constraints: list[str] | None = None) -> FeaturePlan:
    if not isinstance(feature, str) or not feature.strip():
        raise ValueError("feature must be non-empty")
    if not isinstance(requirements, list) or any(not isinstance(x, str) or not x.strip() for x in requirements):
        raise ValueError("requirements must be a list of non-empty strings")
    if constraints is None:
        constraints = []
    if not isinstance(constraints, list) or any(not isinstance(x, str) or not x.strip() for x in constraints):
        raise ValueError("constraints must be a list of non-empty strings")
    scope = tuple(dict.fromkeys(x.strip() for x in requirements))
    phases = (
        ("discovery", ("Confirm user journeys, non-functional requirements, and out-of-scope behavior",)),
        ("design", ("Document API/data contracts, dependencies, failure modes, and security boundaries",)),
        ("implementation", tuple(f"Implement and review: {item}" for item in scope) or ("Break the feature into reviewed vertical slices",)),
        ("verification", ("Add unit, integration, negative, and regression tests", "Validate performance and observability requirements")),
        ("release", ("Use a reversible, observable rollout with an owner and rollback trigger",)),
    )
    quality = (
        "Input validation and authorization are explicit",
        "Errors are actionable and do not leak secrets",
        "Idempotency, retries, and concurrency are addressed where relevant",
        "Logs, metrics, and traces support diagnosis",
    )
    rollout = (
        "Confirm dashboards, alerts, and baseline metrics before release",
        "Release behind a feature flag or staged exposure where practical",
        "Define rollback criteria and verify rollback procedure",
    )
    unresolved = tuple(constraints) if constraints else ("No constraints supplied; confirm scale, compatibility, deadline, and operational ownership",)
    return FeaturePlan(feature.strip(), scope, phases, quality, rollout, unresolved)


def to_json(plan: FeaturePlan) -> str:
    return json.dumps(asdict(plan), indent=2)


if __name__ == "__main__":
    print(to_json(plan_feature("Export reports", ["Generate CSV", "Authorize downloads"])))
