"""Linear capacity trend estimate; use as planning guidance, not a guarantee."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Forecast:
    resource: str
    current_percent: float
    daily_change_percent: float
    days_to_threshold: float | None
    status: str

def forecast_capacity(samples: list[dict], *, threshold_percent: float=85.0) -> list[Forecast]:
    if not isinstance(samples,list): raise TypeError("samples must be a list")
    if not 0<threshold_percent<=100: raise ValueError("threshold_percent must be in (0,100]")
    grouped={}
    for i,s in enumerate(samples):
        if not isinstance(s,dict): raise ValueError(f"sample {i} must be an object")
        name=s.get("resource"); day=s.get("day"); value=s.get("utilization_percent")
        if not isinstance(name,str) or not name.strip(): raise ValueError(f"sample {i} requires resource")
        if isinstance(day,bool) or not isinstance(day,int) or day<0: raise ValueError("day must be a non-negative integer")
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not 0<=value<=100: raise ValueError("utilization_percent must be in [0,100]")
        grouped.setdefault(name,[]).append((day,float(value)))
    results=[]
    for name,points in sorted(grouped.items()):
        points.sort();
        if len({p[0] for p in points})!=len(points): raise ValueError(f"duplicate sample day for {name}")
        current=points[-1][1]
        if len(points)<2: slope=0.0
        else:
            dx=points[-1][0]-points[0][0]; slope=(points[-1][1]-points[0][1])/dx if dx else 0.0
        days=(threshold_percent-current)/slope if slope>0 and current<threshold_percent else (0.0 if current>=threshold_percent else None)
        status="threshold_reached" if current>=threshold_percent else "approaching" if days is not None and days<=30 else "stable_or_declining" if slope<=0 else "within_capacity"
        results.append(Forecast(name,current,round(slope,3),None if days is None else round(days,1),status))
    return results
