"""Calculate free intervals from timezone-aware calendar events."""
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Event:
    start:datetime
    end:datetime

@dataclass(frozen=True)
class Slot:
    start:datetime
    end:datetime

def free_slots(window_start:datetime,window_end:datetime,events:list[Event])->list[Slot]:
    if window_start.tzinfo is None or window_end.tzinfo is None or window_start>=window_end:
        raise ValueError("window must be ordered and timezone-aware")
    normalized=[]
    for event in events:
        if event.start.tzinfo is None or event.end.tzinfo is None or event.start>=event.end:
            raise ValueError("events must be ordered and timezone-aware")
        start=max(window_start,event.start); end=min(window_end,event.end)
        if start<end: normalized.append((start,end))
    normalized.sort()
    merged=[]
    for start,end in normalized:
        if merged and start<=merged[-1][1]:
            merged[-1]=(merged[-1][0],max(merged[-1][1],end))
        else: merged.append((start,end))
    result=[]; cursor=window_start
    for start,end in merged:
        if cursor<start: result.append(Slot(cursor,start))
        cursor=max(cursor,end)
    if cursor<window_end: result.append(Slot(cursor,window_end))
    return result
