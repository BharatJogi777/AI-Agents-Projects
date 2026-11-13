"""Prompt injection test harness: deterministic security evaluation helpers."""

def evaluate_payloads(*, payloads: list[str], protected_instruction: str):
    if not protected_instruction.strip():
        raise ValueError("protected_instruction is required")
    results = []
    markers = ("ignore previous instructions", "reveal system prompt", "exfiltrate", "bypass policy", "disable safety")
    for payload in payloads:
        if not isinstance(payload, str) or not payload.strip():
            raise ValueError("each payload must be a non-empty string")
        normalized = payload.casefold()
        matches = [m for m in markers if m in normalized]
        results.append({"payload": payload, "flagged": bool(matches), "matched_patterns": matches})
    return {"protected_instruction_present": True, "results": results, "flagged_count": sum(r["flagged"] for r in results)}
