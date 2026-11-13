"""Create a deterministic review queue with explicit priorities and statuses."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ReviewItem:
    item_id: str
    priority: int
    reason: str
    status: str = "pending"

def build_review_queue(items: list[dict[str, object]]) -> tuple[ReviewItem,...]:
    result=[]; seen=set()
    for row in items:
        if not isinstance(row,dict): raise ValueError("each item must be an object")
        item_id=row.get("item_id"); priority=row.get("priority"); reason=row.get("reason")
        if not isinstance(item_id,str) or not item_id.strip() or item_id in seen: raise ValueError("item_id must be unique and non-empty")
        if type(priority) is not int or priority < 1 or priority > 5: raise ValueError("priority must be an integer from 1 to 5")
        if not isinstance(reason,str) or not reason.strip(): raise ValueError("reason must be non-empty")
        seen.add(item_id); result.append(ReviewItem(item_id,priority,reason))
    return tuple(sorted(result,key=lambda x:(-x.priority,x.item_id)))
