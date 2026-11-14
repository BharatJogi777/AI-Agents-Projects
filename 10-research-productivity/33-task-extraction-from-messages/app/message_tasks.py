"""Extract explicit action statements from supplied message text."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class ExtractedTask:
    message_id: str
    task_text: str
    confidence: str

_ACTION=re.compile(r"^(?:please\s+)?(?:I will|we will|you need to|please|action item:|todo:)\s+(.+)$",re.I)

def extract_tasks(*, messages: list[dict[str,str]]) -> tuple[ExtractedTask,...]:
    if not isinstance(messages,list): raise ValueError("messages must be a list")
    result=[]; seen=set()
    for m in messages:
        if not isinstance(m,dict) or not isinstance(m.get("id"),str) or not m["id"].strip() or not isinstance(m.get("text"),str): raise ValueError("each message needs id and text")
        if m["id"] in seen: raise ValueError("message IDs must be unique")
        seen.add(m["id"])
        for line in m["text"].splitlines():
            match=_ACTION.match(line.strip())
            if match and match.group(1).strip(): result.append(ExtractedTask(m["id"],match.group(1).strip(),"heuristic"))
    return tuple(result)
