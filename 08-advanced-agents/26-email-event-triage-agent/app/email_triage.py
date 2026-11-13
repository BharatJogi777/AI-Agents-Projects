"""Deterministic email event triage; does not send, archive, or delete mail."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Email:
    message_id: str
    sender: str
    subject: str
    received_at: str
    labels: tuple[str, ...] = ()

@dataclass(frozen=True)
class EmailDecision:
    message_id: str
    priority: str
    reason: str
    action: str

def triage_emails(messages: list[Email]) -> tuple[EmailDecision, ...]:
    seen, out = set(), []
    for msg in messages:
        if not msg.message_id.strip() or msg.message_id in seen:
            raise ValueError("message IDs must be non-empty and unique")
        seen.add(msg.message_id)
        if "@" not in msg.sender or not msg.sender.rsplit("@", 1)[1]:
            raise ValueError("sender must be an email address")
        if not msg.subject.strip() or not msg.received_at.strip():
            raise ValueError("subject and received_at are required")
        text = (msg.subject + " " + " ".join(msg.labels)).lower()
        if any(term in text for term in ("security", "breach", "outage", "urgent", "failed payment")):
            priority, reason = "high", "Potentially time-sensitive subject or label"
        elif any(term in text for term in ("newsletter", "promotion", "unsubscribe")):
            priority, reason = "low", "Likely bulk or promotional email"
        else:
            priority, reason = "normal", "No configured priority signal"
        out.append(EmailDecision(msg.message_id, priority, reason, "human_review"))
    return tuple(out)
