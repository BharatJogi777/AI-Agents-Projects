"""Summarize repeated test outcomes to surface instability signals."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import json
from statistics import mean, pstdev


@dataclass(frozen=True)
class TestStability:
    test_id: str
    runs: int
    failures: int
    failure_rate: float
    duration_mean: float
    duration_stddev: float
    suspected_flaky: bool


def analyze_runs(records: list[dict], failure_threshold: float = 0.0) -> list[TestStability]:
    if not isinstance(records, list):
        raise TypeError("records must be a list")
    if not 0 <= failure_threshold <= 1:
        raise ValueError("failure_threshold must be between 0 and 1")
    grouped: dict[str, list[dict]] = {}
    for item in records:
        if not isinstance(item, dict) or not isinstance(item.get("test_id"), str) or not item["test_id"]:
            raise ValueError("each record requires a non-empty test_id")
        if item.get("outcome") not in ("passed", "failed"):
            raise ValueError("outcome must be passed or failed")
        duration = item.get("duration")
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) or duration < 0:
            raise ValueError("duration must be a non-negative number")
        grouped.setdefault(item["test_id"], []).append(item)
    result = []
    for test_id, runs in sorted(grouped.items()):
        failures = sum(r["outcome"] == "failed" for r in runs)
        rate = failures / len(runs)
        durations = [float(r["duration"]) for r in runs]
        result.append(TestStability(test_id, len(runs), failures, rate, mean(durations),
                                    pstdev(durations), 0 < rate < 1 or rate > failure_threshold and rate > 0))
    return result


def to_json(results: list[TestStability]) -> str:
    return json.dumps([asdict(item) for item in results], indent=2)


if __name__ == "__main__":
    sample = [{"test_id": "test_api", "outcome": "passed", "duration": 0.2},
              {"test_id": "test_api", "outcome": "failed", "duration": 0.8}]
    print(to_json(analyze_runs(sample)))
