"""Explainable heuristic issue triage."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class TriageResult:
    category: str
    urgency: str
    confidence: float
    labels: tuple[str, ...]
    routing_hint: str
    evidence: tuple[str, ...]


CATEGORY_RULES = {
    "bug": ("bug", "crash", "exception", "traceback", "does not work", "regression", "broken"),
    "security": ("vulnerability", "cve", "unauthorized", "authentication bypass", "exposed secret", "injection"),
    "performance": ("slow", "latency", "memory leak", "high cpu", "timeout", "throughput"),
    "documentation": ("readme", "documentation", "typo", "example is unclear", "docs"),
    "feature": ("please add", "feature request", "would be useful", "support for"),
}


def classify_issue(title: str, body: str = "") -> TriageResult:
    if not isinstance(title, str) or not title.strip() or not isinstance(body, str):
        raise ValueError("title must be non-empty and body must be text")
    text = f"{title}\n{body}".lower()
    scores = {category: [term for term in terms if term in text] for category, terms in CATEGORY_RULES.items()}
    ranked = sorted(((len(matches), category, matches) for category, matches in scores.items()), reverse=True)
    count, category, matches = ranked[0]
    if count == 0:
        category, confidence, evidence = "needs-triage", 0.25, ()
    else:
        confidence = min(0.95, 0.45 + 0.15 * count)
        evidence = tuple(matches)
    urgent_terms = ("data loss", "production down", "actively exploited", "security breach", "service unavailable")
    urgency = "critical" if any(term in text for term in urgent_terms) else (
        "high" if category == "security" else "normal"
    )
    labels = (category, f"priority:{urgency}")
    routing = {"security": "security-maintainers", "performance": "runtime-maintainers",
               "documentation": "documentation-maintainers", "feature": "product-maintainers",
               "bug": "component-maintainers"}.get(category, "triage-queue")
    return TriageResult(category, urgency, confidence, labels, routing, evidence)


def to_json(result: TriageResult) -> str:
    return json.dumps(asdict(result), indent=2)


if __name__ == "__main__":
    print(to_json(classify_issue("Production down: authentication bypass")))
