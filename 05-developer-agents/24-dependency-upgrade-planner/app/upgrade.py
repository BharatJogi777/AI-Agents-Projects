"""Create a conservative dependency upgrade plan from supplied versions."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import json
import re


@dataclass(frozen=True)
class Upgrade:
    package: str
    current: str
    target: str
    change_type: str
    checks: tuple[str, ...]


def _version(value: str) -> tuple[int, int, int]:
    if not isinstance(value, str) or not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise ValueError(f"unsupported version format: {value!r}; expected MAJOR.MINOR.PATCH")
    return tuple(int(part) for part in value.split("."))


def plan_upgrades(current: dict[str, str], targets: dict[str, str]) -> list[Upgrade]:
    if not isinstance(current, dict) or not isinstance(targets, dict):
        raise TypeError("current and targets must be mappings")
    result = []
    for package, target in targets.items():
        if not isinstance(package, str) or not package.strip() or package not in current:
            raise ValueError(f"target package {package!r} is missing from current versions")
        old, new = _version(current[package]), _version(target)
        if new < old:
            kind = "downgrade"
        elif new[0] > old[0]:
            kind = "major"
        elif new[1] > old[1]:
            kind = "minor"
        elif new[2] > old[2]:
            kind = "patch"
        else:
            kind = "unchanged"
        result.append(Upgrade(package, current[package], target, kind, (
            "Read release notes and breaking-change guidance",
            "Check runtime and transitive dependency compatibility",
            "Run unit, integration, security, and performance checks",
            "Prepare rollback and lockfile review",
        )))
    return result


def to_json(items: list[Upgrade]) -> str:
    return json.dumps([asdict(x) for x in items], indent=2)


if __name__ == "__main__":
    print(to_json(plan_upgrades({"fastapi": "0.110.0"}, {"fastapi": "0.111.0"})))
