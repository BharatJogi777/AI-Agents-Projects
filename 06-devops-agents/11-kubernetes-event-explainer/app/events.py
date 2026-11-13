"""Explain Kubernetes event streams using deterministic rules."""
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Any

@dataclass(frozen=True)
class EventFinding:
    namespace: str
    kind: str
    name: str
    reason: str
    count: int
    message: str
    severity: str
    explanation: str

def explain_events(events: list[dict[str, Any]]) -> list[EventFinding]:
    """Group event dictionaries; reject malformed timestamps and missing identity."""
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for index, event in enumerate(events):
        for field in ("namespace", "kind", "name", "reason", "message", "type", "last_timestamp"):
            if field not in event or event[field] in (None, ""):
                raise ValueError(f"event {index}: missing {field}")
        try:
            datetime.fromisoformat(str(event["last_timestamp"]).replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"event {index}: invalid last_timestamp") from exc
        key = (event["namespace"], event["kind"], event["name"], event["reason"])
        groups[key].append(event)
    findings = []
    for (namespace, kind, name, reason), rows in groups.items():
        messages = Counter(str(row["message"]).strip() for row in rows)
        message = messages.most_common(1)[0][0]
        warning = any(str(row["type"]).lower() == "warning" for row in rows)
        severity = "high" if warning and len(rows) >= 5 else "medium" if warning else "info"
        explanation = {
            "FailedScheduling": "The scheduler could not place the workload; inspect resource requests, node selectors, taints, and available capacity.",
            "BackOff": "The container repeatedly failed and Kubernetes is delaying another restart; inspect container logs and termination details.",
            "Unhealthy": "A configured health probe failed; inspect probe configuration and application startup or dependency health.",
            "Failed": "A Kubernetes operation failed; use the event message and related object status to narrow the cause.",
        }.get(reason, "Review the event message and related object status; this reason has no built-in specialized explanation.")
        findings.append(EventFinding(namespace, kind, name, reason, len(rows), message, severity, explanation))
    return sorted(findings, key=lambda item: ({"high": 0, "medium": 1, "info": 2}[item.severity], -item.count, item.namespace, item.name))
