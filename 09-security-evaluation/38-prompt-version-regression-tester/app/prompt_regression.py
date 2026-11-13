"""Evaluate prompt-version outputs against deterministic case expectations."""
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class PromptCase:
    case_id: str
    required_terms: tuple[str, ...] = ()
    forbidden_terms: tuple[str, ...] = ()

@dataclass(frozen=True)
class VersionScore:
    version: str
    passed: int
    total: int
    failed_case_ids: tuple[str, ...]
    @property
    def pass_rate(self) -> float:
        return self.passed / self.total if self.total else 0.0

def score_version(version: str, cases: Iterable[PromptCase], outputs: dict[str, str]) -> VersionScore:
    if not version.strip():
        raise ValueError("version is required")
    case_list = tuple(cases)
    ids = [c.case_id for c in case_list]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError("case IDs must be non-empty and unique")
    if set(outputs) != set(ids):
        raise ValueError("outputs must contain exactly one value per case")
    failed = []
    for case in case_list:
        output = outputs[case.case_id]
        if not isinstance(output, str):
            raise TypeError("outputs must be strings")
        normalized = output.casefold()
        if any(term.casefold() not in normalized for term in case.required_terms) or any(term.casefold() in normalized for term in case.forbidden_terms):
            failed.append(case.case_id)
    return VersionScore(version, len(ids) - len(failed), len(ids), tuple(failed))

def compare_versions(baseline: VersionScore, candidate: VersionScore) -> dict[str, object]:
    if baseline.total != candidate.total:
        raise ValueError("versions must use the same number of cases")
    return {"baseline": baseline.version, "candidate": candidate.version, "pass_rate_delta": candidate.pass_rate - baseline.pass_rate, "new_regressions": tuple(sorted(set(candidate.failed_case_ids) - set(baseline.failed_case_ids)))}
