"""Validate and curate a caller-supplied entity relationship graph."""
from dataclasses import dataclass

@dataclass(frozen=True)
class GraphReport:
    entities: tuple[str, ...]
    relationships: tuple[tuple[str, str, str], ...]
    duplicate_entities: tuple[str, ...]
    dangling_relationships: tuple[tuple[str, str, str], ...]
    self_loops: tuple[tuple[str, str, str], ...]

def curate_graph(*, entities: list[str], relationships: list[tuple[str, str, str]]) -> GraphReport:
    if not isinstance(entities, list) or any(not isinstance(x, str) or not x.strip() for x in entities):
        raise ValueError("entities must contain non-empty strings")
    if not isinstance(relationships, list):
        raise ValueError("relationships must be a list")
    for edge in relationships:
        if not isinstance(edge, tuple) or len(edge) != 3 or any(not isinstance(x, str) or not x.strip() for x in edge):
            raise ValueError("each relationship must be a 3-item tuple of non-empty strings")
    seen, duplicates = set(), []
    for entity in entities:
        name = entity.strip()
        if name in seen and name not in duplicates:
            duplicates.append(name)
        seen.add(name)
    normalized = tuple((s.strip(), p.strip(), o.strip()) for s, p, o in relationships)
    dangling = tuple(e for e in normalized if e[0] not in seen or e[2] not in seen)
    loops = tuple(e for e in normalized if e[0] == e[2])
    return GraphReport(tuple(sorted(seen)), normalized, tuple(sorted(duplicates)), dangling, loops)
