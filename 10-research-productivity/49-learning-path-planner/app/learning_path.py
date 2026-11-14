"""Validate learning prerequisites and produce a stable study sequence."""
from dataclasses import dataclass
@dataclass(frozen=True)
class LearningTopic:
    id:str; title:str; prerequisites:tuple[str,...]=(); estimated_hours:float=1.0
def build_learning_path(topics:list[LearningTopic])->list[LearningTopic]:
    if not topics: raise ValueError("at least one topic is required")
    by_id={}
    for t in topics:
        if not t.id.strip() or not t.title.strip() or t.id in by_id: raise ValueError("topic ids and titles must be non-empty and ids unique")
        if t.estimated_hours<=0: raise ValueError("estimated_hours must be positive")
        by_id[t.id]=t
    for t in topics:
        unknown=set(t.prerequisites)-by_id.keys()
        if unknown: raise ValueError(f"unknown prerequisites for {t.id}: {sorted(unknown)}")
        if t.id in t.prerequisites: raise ValueError("a topic cannot require itself")
    remaining={t.id:set(t.prerequisites) for t in topics}; ordered=[]
    while remaining:
        ready=[t.id for t in topics if t.id in remaining and not remaining[t.id]]
        if not ready: raise ValueError("prerequisite cycle detected")
        for topic_id in ready:
            ordered.append(by_id[topic_id]); remaining.pop(topic_id)
            for deps in remaining.values(): deps.discard(topic_id)
    return ordered
