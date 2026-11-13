from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable

@dataclass(frozen=True)
class ResearchFinding:
    question: str
    answer: str
    sources: tuple[str, ...] = ()

@dataclass(frozen=True)
class ResearchReport:
    findings: tuple[ResearchFinding, ...]
    failures: dict[str, str]

class FanOutFanIn:
    def __init__(self, researcher: Callable[[str], ResearchFinding], max_workers: int = 4):
        if max_workers < 1:
            raise ValueError("max_workers must be positive")
        self.researcher, self.max_workers = researcher, max_workers

    def run(self, questions: list[str]) -> ResearchReport:
        if any(not q.strip() for q in questions):
            raise ValueError("questions cannot be empty")
        if len(questions) != len(set(questions)):
            raise ValueError("questions must be unique")
        findings, failures = {}, {}
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            pending = {pool.submit(self.researcher, q): q for q in questions}
            for future in as_completed(pending):
                question = pending[future]
                try:
                    finding = future.result()
                    if not isinstance(finding, ResearchFinding):
                        raise TypeError("researcher must return ResearchFinding")
                    if finding.question != question:
                        raise ValueError("finding question does not match request")
                    findings[question] = finding
                except Exception as exc:
                    failures[question] = str(exc)
        return ResearchReport(tuple(findings[q] for q in questions if q in findings), failures)
