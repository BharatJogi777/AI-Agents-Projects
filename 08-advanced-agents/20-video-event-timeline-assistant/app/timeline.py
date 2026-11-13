from dataclasses import dataclass
@dataclass(frozen=True)
class Event:
    timestamp:float
    label:str
    description:str
    confidence:float
def build_timeline(duration:float,events:list[Event])->dict:
    if duration<=0: raise ValueError("duration must be positive")
    for e in events:
        if not 0<=e.timestamp<=duration or not e.label.strip() or not e.description.strip() or not 0<=e.confidence<=1:
            raise ValueError("event timestamp, labels, description, or confidence are invalid")
    ordered=sorted(events,key=lambda e:e.timestamp)
    return {"duration_seconds":duration,"events":[e.__dict__ for e in ordered],
            "review_indices":[i for i,e in enumerate(ordered) if e.confidence<0.75]}
