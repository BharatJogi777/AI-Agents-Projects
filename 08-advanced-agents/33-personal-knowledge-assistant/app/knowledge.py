"""Small transparent search over user-provided notes; no facts are synthesized."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Note:
    note_id: str
    text: str

@dataclass(frozen=True)
class Match:
    note_id: str
    score: int
    excerpt: str

def search_notes(notes: list[Note], query: str, *, limit: int = 5) -> tuple[Match, ...]:
    if not query.strip() or limit < 1:
        raise ValueError("query and positive limit are required")
    ids=set()
    terms=set(re.findall(r"[a-z0-9]+",query.lower()))
    if not terms:
        raise ValueError("query must contain searchable terms")
    matches=[]
    for note in notes:
        if not note.note_id.strip() or note.note_id in ids:
            raise ValueError("note IDs must be non-empty and unique")
        ids.add(note.note_id)
        if not note.text.strip():
            raise ValueError("note text cannot be empty")
        tokens=set(re.findall(r"[a-z0-9]+",note.text.lower()))
        score=len(terms & tokens)
        if score:
            excerpt=note.text.strip()
            matches.append(Match(note.note_id,score,excerpt[:240]))
    matches.sort(key=lambda m:(-m.score,m.note_id))
    return tuple(matches[:limit])
