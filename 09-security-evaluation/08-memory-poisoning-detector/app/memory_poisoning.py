"""Memory poisoning detector: deterministic evaluation helper."""

def inspect_memory_entries(*, entries: list[dict[str, str]]):
        results = []
        indicators = ("always ignore", "system prompt", "secret key", "password is", "never tell the user", "override policy")
        for entry in entries:
            if not isinstance(entry, dict) or not isinstance(entry.get("content"), str) or not entry.get("id"):
                raise ValueError("each entry requires id and string content")
            content = entry["content"].casefold()
            hits = [term for term in indicators if term in content]
            results.append({"id": entry["id"], "suspicious": bool(hits), "signals": hits, "recommendation": "quarantine for review" if hits else "retain with provenance"})
        return results
