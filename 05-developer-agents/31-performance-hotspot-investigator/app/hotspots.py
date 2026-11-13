"""Rank sampled performance profiles and flag concentration."""
from collections import defaultdict
def investigate(samples: list[dict], top_n: int = 10) -> list[dict]:
    if top_n < 1: raise ValueError("top_n must be positive")
    totals=defaultdict(float); counts=defaultdict(int)
    for row in samples:
        name=row.get("operation")
        duration=row.get("duration_ms")
        if not isinstance(name,str) or not name.strip(): raise ValueError("operation is required")
        if isinstance(duration,bool) or not isinstance(duration,(int,float)) or duration < 0: raise ValueError("duration_ms must be non-negative")
        totals[name]+=float(duration); counts[name]+=1
    overall=sum(totals.values())
    ranked=[]
    for name,total in totals.items():
        ranked.append({"operation":name,"total_ms":round(total,3),"calls":counts[name],"mean_ms":round(total/counts[name],3),"share":round(total/overall,4) if overall else 0.0})
    return sorted(ranked,key=lambda x:(-x["total_ms"],x["operation"]))[:top_n]
