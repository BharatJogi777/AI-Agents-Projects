from dataclasses import dataclass
@dataclass(frozen=True)
class Stop:
    stop_id: str
    latitude: float
    longitude: float
    demand: int
def validate_route(stops: list[Stop], capacity: int) -> dict:
    if capacity<=0: raise ValueError("capacity must be positive")
    seen=set(); total=0; normalized=[]
    for s in stops:
        if not s.stop_id.strip() or s.stop_id in seen: raise ValueError("stop ids must be non-empty and unique")
        if not -90<=s.latitude<=90 or not -180<=s.longitude<=180: raise ValueError("coordinates out of range")
        if s.demand<0: raise ValueError("demand cannot be negative")
        seen.add(s.stop_id); total+=s.demand
        normalized.append({"stop_id":s.stop_id,"latitude":s.latitude,"longitude":s.longitude,"demand":s.demand})
    return {"stops":normalized,"total_demand":total,"capacity":capacity,"capacity_feasible":total<=capacity,"route_optimized":False,"driver_confirmation_required":True}
