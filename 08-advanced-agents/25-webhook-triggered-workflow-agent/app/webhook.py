"""Verify webhook authenticity and create workflow intents; never execute workflows."""
import hashlib, hmac, time
from dataclasses import dataclass

@dataclass(frozen=True)
class WorkflowIntent:
    event_id: str
    event_type: str
    action: str

ACTIONS = {"invoice.paid": "reconcile_invoice", "ticket.created": "triage_ticket", "deployment.failed": "investigate_deployment"}

def verify_webhook(*, body: bytes, signature: str, secret: str, timestamp: int, now: int | None = None, tolerance_seconds: int = 300, event_id: str, event_type: str, seen_ids: set[str] | None = None) -> WorkflowIntent:
    if not secret or not body:
        raise ValueError("secret and body are required")
    if not event_id.strip():
        raise ValueError("event_id is required")
    if event_type not in ACTIONS:
        raise ValueError("unsupported event type")
    if tolerance_seconds < 0:
        raise ValueError("tolerance_seconds cannot be negative")
    current = int(time.time()) if now is None else now
    if abs(current - timestamp) > tolerance_seconds:
        raise ValueError("webhook timestamp outside tolerance")
    expected = hmac.new(secret.encode(), str(timestamp).encode() + b"." + body, hashlib.sha256).hexdigest()
    supplied = signature.removeprefix("sha256=")
    if not hmac.compare_digest(expected, supplied):
        raise ValueError("invalid webhook signature")
    if event_id in (seen_ids or set()):
        raise ValueError("replayed event")
    return WorkflowIntent(event_id, event_type, ACTIONS[event_type])
