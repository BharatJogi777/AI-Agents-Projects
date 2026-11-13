from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True)
class Stop:
    day: date
    start_minute: int
    end_minute: int
    place: str
    travel_minutes_before: int = 0
def build_itinerary(stops: list[Stop]) -> dict:
    ordered=sorted(stops,key=lambda x:(x.day,x.start_minute,x.place.casefold()))
    previous=None; result=[]
    for s in ordered:
        if not s.place.strip() or not 0<=s.start_minute<1440 or not 0<s.end_minute<=1440 or s.end_minute<=s.start_minute: raise ValueError("invalid stop details or time window")
        if s.travel_minutes_before<0: raise ValueError("travel time cannot be negative")
        if previous and previous.day==s.day and s.start_minute<previous.end_minute+s.travel_minutes_before: raise ValueError("overlapping stops or insufficient travel buffer")
        result.append({"date":s.day.isoformat(),"start_minute":s.start_minute,"end_minute":s.end_minute,"place":s.place.strip(),"travel_minutes_before":s.travel_minutes_before})
        previous=s
    return {"stops":result,"booking_performed":False,"traveler_confirmation_required":True}
