"""Find exact and normalized duplicate text records."""
from dataclasses import dataclass
import re
import hashlib

@dataclass(frozen=True)
class DuplicateGroup:
    fingerprint: str
    record_ids: tuple[str, ...]

def _normalize(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.casefold()))

def detect_duplicates(*, records: list[dict[str, str]]) -> tuple[DuplicateGroup, ...]:
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    groups={}; ids=set()
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get("id"), str) or not record["id"].strip() or not isinstance(record.get("text"), str):
            raise ValueError("each record needs a non-empty id and text string")
        rid=record["id"]
        if rid in ids:
            raise ValueError("record IDs must be unique")
        ids.add(rid)
        normalized=_normalize(record["text"])
        if normalized:
            fingerprint=hashlib.sha256(normalized.encode()).hexdigest()
            groups.setdefault(fingerprint, []).append(rid)
    return tuple(DuplicateGroup(key, tuple(sorted(value))) for key,value in sorted(groups.items()) if len(value)>1)
