"""Detect changes in supplied standards and regulation records."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Update:
    record_id: str
    change: str
    previous_version: str | None
    current_version: str | None
    review_required: bool

def review_updates(*, previous: dict[str, dict[str, str]], current: dict[str, dict[str, str]]) -> tuple[Update, ...]:
    """Compare caller-provided records; does not fetch or interpret regulations."""
    for label, records in (("previous", previous), ("current", current)):
        if not isinstance(records, dict):
            raise ValueError(f"{label} must be a mapping")
        for key, value in records.items():
            if not isinstance(key, str) or not key.strip() or not isinstance(value, dict):
                raise ValueError(f"{label} contains an invalid record")
            if any(not isinstance(k, str) or not isinstance(v, str) for k, v in value.items()):
                raise ValueError(f"{label} record fields must be strings")
    result = []
    for key in sorted(set(previous) | set(current)):
        old, new = previous.get(key), current.get(key)
        if old is None:
            result.append(Update(key, "added", None, new.get("version"), True))
        elif new is None:
            result.append(Update(key, "removed", old.get("version"), None, True))
        elif old != new:
            result.append(Update(key, "changed", old.get("version"), new.get("version"), True))
    return tuple(result)
