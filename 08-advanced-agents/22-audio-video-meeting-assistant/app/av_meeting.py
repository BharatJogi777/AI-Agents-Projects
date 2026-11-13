"""Align supplied meeting media markers; no speech or video inference is performed."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Marker:
    marker_id: str
    media: str
    start_ms: int
    end_ms: int
    content: str

@dataclass(frozen=True)
class Timeline:
    markers: tuple[Marker, ...]
    duration_ms: int
    overlaps: tuple[tuple[str, str], ...]

def build_timeline(markers: list[Marker]) -> Timeline:
    if not markers:
        raise ValueError("at least one marker is required")
    ids = set()
    for m in markers:
        if not m.marker_id.strip() or m.marker_id in ids:
            raise ValueError("marker IDs must be non-empty and unique")
        ids.add(m.marker_id)
        if m.media not in {"audio", "video", "transcript"}:
            raise ValueError("media must be audio, video, or transcript")
        if m.start_ms < 0 or m.end_ms <= m.start_ms:
            raise ValueError("invalid marker time range")
        if not m.content.strip():
            raise ValueError("marker content is required")
    ordered = tuple(sorted(markers, key=lambda m: (m.start_ms, m.end_ms, m.marker_id)))
    overlaps = []
    for i, left in enumerate(ordered):
        for right in ordered[i+1:]:
            if right.start_ms >= left.end_ms:
                break
            if left.media != right.media:
                overlaps.append((left.marker_id, right.marker_id))
    return Timeline(ordered, max(m.end_ms for m in ordered), tuple(overlaps))
