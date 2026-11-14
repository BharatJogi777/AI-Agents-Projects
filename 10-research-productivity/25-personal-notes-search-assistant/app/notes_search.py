"""Search supplied notes using explainable token matching."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class NoteMatch:
    note_id: str
    score: int
    matched_terms: tuple[str, ...]
    text: str

def _tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.lower()))

def search_notes(*, notes: list[dict[str, str]], query: str, limit: int = 10) -> tuple[NoteMatch, ...]:
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be non-empty")
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ValueError("limit must be a positive integer")
    if not isinstance(notes, list):
        raise ValueError("notes must be a list")
    terms = _tokens(query)
    if not terms:
        raise ValueError("query must contain searchable characters")
    matches, seen = [], set()
    for note in notes:
        if not isinstance(note, dict) or not all(isinstance(note.get(k), str) and note[k].strip() for k in ("id", "text")):
            raise ValueError("each note must contain non-empty string id and text")
        if note["id"] in seen:
            raise ValueError("note IDs must be unique")
        seen.add(note["id"])
        found = terms & _tokens(note["text"])
        if found:
            matches.append(NoteMatch(note["id"], len(found), tuple(sorted(found)), note["text"]))
    return tuple(sorted(matches, key=lambda item: (-item.score, item.note_id))[:limit])
