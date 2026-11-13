"""Static preflight checks for unified diff text."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class PatchIssue:
    code: str
    severity: str
    message: str
    line_number: int | None


def validate_patch(patch: str) -> list[PatchIssue]:
    if not isinstance(patch, str):
        raise TypeError("patch must be text")
    lines = patch.splitlines()
    issues: list[PatchIssue] = []
    has_file_header = False
    for index, line in enumerate(lines, 1):
        if line.startswith("diff --git "):
            has_file_header = True
        if line.startswith("+++ ") or line.startswith("--- "):
            path = line[4:].split("\t", 1)[0]
            if path not in ("/dev/null",) and (path.startswith("/") or ".." in path.replace("\\", "/").split("/")):
                issues.append(PatchIssue("unsafe-path", "high", "Patch references an absolute or parent-traversal path", index))
        if line.endswith((" ", "\t")) and line[:1] in ("+", "-"):
            issues.append(PatchIssue("trailing-whitespace", "low", "Changed line has trailing whitespace", index))
        if line.startswith("GIT binary patch") or line.startswith("Binary files "):
            issues.append(PatchIssue("binary-change", "medium", "Binary patch requires separate review", index))
        if line.startswith("rename from ") or line.startswith("rename to "):
            issues.append(PatchIssue("rename", "medium", "Rename metadata requires path review", index))
    if patch.strip() and not has_file_header:
        issues.append(PatchIssue("missing-diff-header", "medium", "No Git diff file header found", None))
    return issues


def to_json(issues: list[PatchIssue]) -> str:
    return json.dumps([asdict(item) for item in issues], indent=2)


if __name__ == "__main__":
    print(to_json(validate_patch("diff --git a/a.py b/a.py\n--- a/a.py\n+++ b/a.py\n")))
