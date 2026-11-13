"""Deterministic inbox event triage; never performs mailbox actions."""
from dataclasses import dataclass

@dataclass(frozen=True)
class InboxEvent:
    event_id: str
    sender: str
    subject: str
    received_at: str
    body_preview: str = ""

@dataclass(frozen=True)
class Triage:
    event_id: str
    category: str
    priority: str
    recommendation: str
    requires_human_review: bool

def triage_inbox(events: list[InboxEvent], *, trusted_domains: set[str] | None = None) -> tuple[Triage, ...]:
    trusted_domains = trusted_domains or set()
    seen, results = set(), []
    for event in events:
        if not event.event_id.strip() or event.event_id in seen:
            raise ValueError("event IDs must be non-empty and unique")
        seen.add(event.event_id)
        if "@" not in event.sender or not event.sender.rsplit("@",1)[1]:
            raise ValueError("sender must be an email address")
        if not event.subject.strip() or not event.received_at.strip():
            raise ValueError("subject and received_at are required")
        domain = event.sender.rsplit("@",1)[1].lower()
        text = (event.subject + " " + event.body_preview).lower()
        if any(word in text for word in ("urgent", "outage", "security incident", "payment failed")):
            category, priority, recommendation = "action_required", "high", "Review promptly; do not auto-reply"
        elif any(word in text for word in ("unsubscribe", "promotion", "sale")):
            category, priority, recommendation = "promotion", "low", "Review before applying a mailbox rule"
        else:
            category, priority, recommendation = "general", "normal", "Read and decide whether a response is needed"
        trusted = domain in {d.lower() for d in trusted_domains}
        results.append(Triage(event.event_id, category, priority, recommendation, not trusted or priority == "high"))
    return tuple(results)
