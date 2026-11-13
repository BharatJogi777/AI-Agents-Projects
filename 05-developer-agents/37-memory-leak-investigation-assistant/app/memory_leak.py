"""Summarize memory samples and detect monotonic growth."""
def investigate(samples: list[dict], min_growth_mb: float=1.0) -> dict:
    if min_growth_mb<0: raise ValueError("min_growth_mb cannot be negative")
    if not samples: raise ValueError("At least one sample is required")
    values=[]
    for row in samples:
        value=row.get("memory_mb")
        if isinstance(value,bool) or not isinstance(value,(int,float)) or value<0: raise ValueError("memory_mb must be non-negative")
        values.append(float(value))
    deltas=[round(b-a,3) for a,b in zip(values,values[1:])]
    growth=round(values[-1]-values[0],3)
    sustained=bool(deltas) and all(x>0 for x in deltas) and growth>=min_growth_mb
    return {"start_mb":values[0],"end_mb":values[-1],"net_growth_mb":growth,"deltas_mb":deltas,"sustained_growth":sustained,"assessment":"Investigate retained references and lifecycle cleanup" if sustained else "Insufficient evidence of monotonic growth"}
