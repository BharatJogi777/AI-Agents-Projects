"""Generate integration scenarios from declared service dependencies."""
from __future__ import annotations
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Scenario:
    name: str
    boundary: str
    setup: str
    action: str
    assertion: str
    cleanup: str


def plan_integration_tests(services: list[str], dependencies: dict[str, list[str]]) -> list[Scenario]:
    if not isinstance(services, list) or not services or any(not isinstance(x, str) or not x.strip() for x in services):
        raise ValueError("services must be a non-empty list of names")
    if len(set(services)) != len(services):
        raise ValueError("service names must be unique")
    if not isinstance(dependencies, dict):
        raise TypeError("dependencies must be a mapping")
    known = set(services)
    for service, deps in dependencies.items():
        if service not in known or not isinstance(deps, list) or any(dep not in known for dep in deps):
            raise ValueError(f"invalid dependency declaration for {service}")
    result = []
    for service in services:
        for dependency in dependencies.get(service, []):
            boundary = f"{service} -> {dependency}"
            result.extend((
                Scenario(f"{service}_calls_{dependency}_success", boundary, f"Start {dependency} fixture", f"Invoke {service}", "Assert valid response and expected state", "Reset fixture and test data"),
                Scenario(f"{service}_calls_{dependency}_timeout", boundary, f"Delay {dependency} beyond timeout", f"Invoke {service}", "Assert bounded timeout and safe error mapping", "Stop fixture and clear pending work"),
                Scenario(f"{service}_calls_{dependency}_failure", boundary, f"Return controlled failure from {dependency}", f"Invoke {service}", "Assert retry policy and no duplicate side effect", "Reset fixture and test data"),
            ))
    return result


def to_json(scenarios: list[Scenario]) -> str:
    return json.dumps([asdict(item) for item in scenarios], indent=2)


if __name__ == "__main__":
    print(to_json(plan_integration_tests(["api", "payments"], {"api": ["payments"]})))
