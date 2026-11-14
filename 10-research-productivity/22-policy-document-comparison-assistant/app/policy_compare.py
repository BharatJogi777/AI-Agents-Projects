"""Compare policy sections without interpreting legal effect."""
from dataclasses import dataclass

@dataclass(frozen=True)
class SectionChange:
    section_id: str
    change: str
    before: str | None
    after: str | None

def compare_policies(*, before: dict[str, str], after: dict[str, str]) -> tuple[SectionChange, ...]:
    """Return deterministic section-level differences; inputs are caller supplied."""
    for label, document in (("before", before), ("after", after)):
        if not isinstance(document, dict):
            raise ValueError(f"{label} must be a mapping of section IDs to text")
        if any(not isinstance(k, str) or not k.strip() or not isinstance(v, str) for k, v in document.items()):
            raise ValueError(f"{label} contains an invalid section")
    changes = []
    for key in sorted(set(before) | set(after)):
        old, new = before.get(key), after.get(key)
        if old is None:
            changes.append(SectionChange(key, "added", None, new))
        elif new is None:
            changes.append(SectionChange(key, "removed", old, None))
        elif old != new:
            changes.append(SectionChange(key, "modified", old, new))
    return tuple(changes)
