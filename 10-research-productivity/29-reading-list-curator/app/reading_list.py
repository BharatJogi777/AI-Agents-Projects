"""Curate a reading list by status, priority, and due date."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ReadingItem:
    item_id: str
    title: str
    status: str
    priority: int
    due_date: str

def curate_reading_list(*, items: list[dict]) -> tuple[ReadingItem,...]:
    if not isinstance(items,list): raise ValueError("items must be a list")
    result=[]; seen=set()
    for item in items:
        if not isinstance(item,dict): raise ValueError("each item must be a mapping")
        rid,title,status,priority,due=(item.get(k) for k in ("id","title","status","priority","due_date"))
        if not all(isinstance(v,str) and v.strip() for v in (rid,title,status,due)): raise ValueError("id, title, status and due_date must be non-empty strings")
        if rid in seen: raise ValueError("item IDs must be unique")
        if status not in ("unread","reading","completed","deferred"): raise ValueError("unsupported reading status")
        if not isinstance(priority,int) or isinstance(priority,bool) or not 1<=priority<=5: raise ValueError("priority must be an integer from 1 to 5")
        seen.add(rid); result.append(ReadingItem(rid,title.strip(),status,priority,due))
    return tuple(sorted(result,key=lambda x:(x.status!="reading",x.status=="completed",-x.priority,x.due_date,x.item_id)))
