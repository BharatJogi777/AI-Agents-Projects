"""Safe, deterministic heuristic review of unified diffs."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    message: str
    file_path: str
    line_number: int | None
    evidence: str


RULES = (
    ("debug-output", "low", re.compile(r"\b(?:print\s*\(|console\.log\s*\(|debugger\s*;)"), "Debug output left in changed code"),
    ("broad-exception", "medium", re.compile(r"\bexcept\s*:\s*$|\bcatch\s*\(\s*(?:Exception|Throwable)\b"), "Broad exception handling can hide failures"),
    ("tls-disabled", "high", re.compile(r"(?:verify\s*=\s*False|rejectUnauthorized\s*:\s*false)"), "TLS certificate verification appears disabled"),
    ("embedded-secret", "high", re.compile(r"(?i)(?:api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]"), "Possible hard-coded secret; rotate if genuine"),
    ("destructive-shell", "high", re.compile(r"(?i)\b(?:rm\s+-rf\s+/(?:\s|$)|DROP\s+DATABASE|mkfs\.)"), "Potentially destructive command in changed content"),
)


def parse_added_lines(diff: str) -> list[tuple[str, int, str]]:
    """Return (path, new_line_number, content) for added non-header lines."""
    if not isinstance(diff, str):
        raise TypeError("diff must be a string")
    path, new_line, result = "", 0, []
    for line in diff.splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else line[4:]
            if path == "/dev/null":
                path = ""
        elif line.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,(\d+))?", line)
            if match:
                new_line = int(match.group(1))
        elif line.startswith("+") and not line.startswith("+++"):
            if path:
                result.append((path, new_line, line[1:]))
            new_line += 1
        elif line.startswith(" ") and not line.startswith("+++"):
            new_line += 1
    return result


def review_diff(diff: str, minimum_severity: str = "low") -> list[Finding]:
    levels = {"low": 1, "medium": 2, "high": 3}
    if minimum_severity not in levels:
        raise ValueError("minimum_severity must be low, medium, or high")
    findings: list[Finding] = []
    for path, number, content in parse_added_lines(diff):
        for rule_id, severity, pattern, message in RULES:
            if levels[severity] >= levels[minimum_severity] and pattern.search(content):
                findings.append(Finding(rule_id, severity, message, path, number, content.strip()[:240]))
    return findings


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("diff", type=Path)
    parser.add_argument("--minimum-severity", choices=("low", "medium", "high"), default="low")
    args = parser.parse_args(argv)
    try:
        findings = review_diff(args.diff.read_text(encoding="utf-8"), args.minimum_severity)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps([asdict(item) for item in findings], indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
