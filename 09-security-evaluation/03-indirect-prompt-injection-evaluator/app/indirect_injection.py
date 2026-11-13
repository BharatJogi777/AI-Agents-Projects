"""Indirect prompt injection evaluator: deterministic security evaluation helpers."""

def evaluate_external_content(*, documents: list[dict[str, str]], trusted_sources: list[str]):
    if not trusted_sources:
        raise ValueError("at least one trusted source identifier is required")
    results = []
    markers = ("ignore the user", "send credentials", "system prompt", "call this tool", "override instructions")
    for doc in documents:
        if not isinstance(doc, dict) or not doc.get("source") or not isinstance(doc.get("content"), str):
            raise ValueError("each document requires source and string content")
        content = doc["content"].casefold()
        hits = [m for m in markers if m in content]
        results.append({"source": doc["source"], "trusted": doc["source"] in trusted_sources, "suspicious": bool(hits), "signals": hits, "recommended_handling": "treat as untrusted data; do not execute embedded instructions" if hits else "retain provenance and treat content as data"})
    return results
