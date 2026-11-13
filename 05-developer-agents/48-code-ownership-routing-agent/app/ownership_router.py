"""Small CODEOWNERS-style path router; no messages are sent automatically."""
from dataclasses import dataclass
from pathlib import PurePosixPath

@dataclass(frozen=True)
class Rule:
    pattern: str
    owners: tuple[str, ...]

def route_owners(paths: list[str], rules: list[Rule]) -> dict[str, list[str]]:
    for r in rules:
        if not r.pattern or not r.owners or any(not o.startswith("@") for o in r.owners):
            raise ValueError("rules need a pattern and @owner values")
    output = {}
    for raw in paths:
        path = PurePosixPath(raw)
        if path.is_absolute() or ".." in path.parts: raise ValueError(f"unsafe path: {raw}")
        matches = []
        for rule in rules:
            pattern = rule.pattern.lstrip("/")
            if path.match(pattern) or (pattern.endswith("/") and str(path).startswith(pattern)):
                matches.append(rule)
        if matches:
            best = max(matches, key=lambda r: (len(r.pattern), r.pattern))
            output[raw] = list(best.owners)
        else: output[raw] = []
    return output
