"""Inspect structured concurrency symptoms and produce review prompts."""
from collections import Counter
RISK_HINTS={
 "shared_mutable_state":"Multiple workers may mutate shared state; require a lock or ownership model",
 "unbounded_fanout":"Unbounded task creation can exhaust memory or downstream capacity",
 "missing_timeout":"Blocking operations need deadlines or cancellation",
 "fire_and_forget":"Detached work may lose errors and outlive its request",
 "non_idempotent_retry":"Retries of side effects require idempotency or deduplication",
 "lock_order":"Inconsistent lock acquisition order can deadlock",
}
def investigate(observations: list[dict]) -> list[dict]:
    findings=[]; seen=set()
    for item in observations:
        kind=item.get("kind")
        if kind not in RISK_HINTS: raise ValueError(f"Unsupported observation kind: {kind!r}")
        location=str(item.get("location","")).strip()
        if not location: raise ValueError("Each observation requires a location")
        key=(kind,location)
        if key in seen: continue
        seen.add(key)
        findings.append({"risk":kind,"location":location,"severity":"high" if kind in {"shared_mutable_state","lock_order","non_idempotent_retry"} else "medium","recommendation":RISK_HINTS[kind]})
    return findings
