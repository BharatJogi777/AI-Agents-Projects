from dataclasses import dataclass
from datetime import datetime,timedelta
@dataclass(frozen=True)
class Slot:
    start: datetime
    end: datetime
def find_common_slots(calendars: dict[str,list[Slot]], duration_minutes: int, window: Slot) -> list[Slot]:
    if duration_minutes<=0: raise ValueError("duration_minutes must be positive")
    if window.end<=window.start: raise ValueError("invalid search window")
    busy=[]
    for owner,slots in calendars.items():
        if not owner.strip(): raise ValueError("calendar owner is required")
        for s in slots:
            if s.end<=s.start: raise ValueError("busy slot end must follow start")
            if s.start.tzinfo!=window.start.tzinfo or s.end.tzinfo!=window.start.tzinfo: raise ValueError("timezone awareness must match the search window")
            if s.start<window.end and s.end>window.start: busy.append(s)
    busy.sort(key=lambda s:s.start); merged=[]
    for s in busy:
        if merged and s.start<=merged[-1].end:
            prev=merged[-1]; merged[-1]=Slot(prev.start,max(prev.end,s.end))
        else: merged.append(s)
    free=[]; cursor=window.start
    for s in merged:
        if s.start>cursor: free.append(Slot(cursor,s.start))
        cursor=max(cursor,s.end)
    if cursor<window.end: free.append(Slot(cursor,window.end))
    duration=timedelta(minutes=duration_minutes)
    return [s for s in free if s.end-s.start>=duration]
