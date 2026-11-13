from dataclasses import dataclass
from statistics import mean
@dataclass(frozen=True)
class DemandObservation:
    period: str
    units: int
def forecast(observations: list[DemandObservation], window: int = 3, safety_stock: int = 0) -> dict:
    if not 1<=window<=len(observations): raise ValueError("window must fit available observations")
    if safety_stock<0: raise ValueError("safety_stock cannot be negative")
    seen=set(); values=[]
    for o in observations:
        if not o.period.strip() or o.period in seen: raise ValueError("periods must be non-empty and unique")
        if o.units<0: raise ValueError("demand cannot be negative")
        seen.add(o.period); values.append(o.units)
    baseline=mean(values[-window:])
    return {"method":"simple_moving_average","periods_used":[o.period for o in observations[-window:]],"baseline_units":baseline,"suggested_plan_units":int(round(baseline+safety_stock)),"safety_stock":safety_stock,"purchase_order_created":False}
