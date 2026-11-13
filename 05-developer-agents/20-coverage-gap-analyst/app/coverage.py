"""Analyze coverage.py JSON data against an explicit source inventory."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class CoverageGap:
    path: str
    executable_lines: int
    missing_lines: int
    coverage_percent: float | None
    status: str


def analyze_coverage(source_files: list[str], report: dict) -> list[CoverageGap]:
    if not isinstance(source_files, list) or any(not isinstance(p, str) or not p.strip() for p in source_files):
        raise ValueError("source_files must be a list of non-empty paths")
    if not isinstance(report, dict) or not isinstance(report.get("files"), dict):
        raise ValueError("report must contain a files mapping from coverage JSON")
    result = []
    for path in dict.fromkeys(source_files):
        entry = report["files"].get(path)
        if entry is None:
            result.append(CoverageGap(path, 0, 0, None, "not-measured"))
            continue
        summary = entry.get("summary", {})
        total = summary.get("num_statements", 0)
        missing = summary.get("missing_lines", 0)
        if any(isinstance(v, bool) or not isinstance(v, int) or v < 0 for v in (total, missing)) or missing > total:
            raise ValueError(f"invalid coverage summary for {path}")
        percent = 100.0 if total == 0 else round((total - missing) / total * 100, 2)
        result.append(CoverageGap(path, total, missing, percent, "covered" if missing == 0 else "gap"))
    return sorted(result, key=lambda item: (
        item.coverage_percent is not None,
        item.coverage_percent if item.coverage_percent is not None else -1,
        -item.missing_lines,
        item.path,
    ))


def to_json(gaps: list[CoverageGap]) -> str:
    return json.dumps([asdict(item) for item in gaps], indent=2)


if __name__ == "__main__":
    sample = {"files": {"app.py": {"summary": {"num_statements": 10, "missing_lines": 3}}}}
    print(to_json(analyze_coverage(["app.py", "new.py"], sample)))
