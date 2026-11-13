from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True)
class Task:
    task_id: str
    field_id: str
    activity: str
    planned_date: date
    duration_hours: float
    required_workers: int
def validate_plan(tasks: list[Task], worker_capacity: dict[date,int]) -> dict:
    seen=set(); by_day={}; rows=[]
    for day,cap in worker_capacity.items():
        if cap<0: raise ValueError("worker capacity cannot be negative")
    for t in tasks:
        if not all(v.strip() for v in (t.task_id,t.field_id,t.activity)) or t.task_id in seen: raise ValueError("task identifiers and details must be non-empty and unique")
        if t.duration_hours<=0 or t.required_workers<=0: raise ValueError("duration and worker count must be positive")
        seen.add(t.task_id); by_day[t.planned_date]=by_day.get(t.planned_date,0)+t.required_workers
        rows.append({"task_id":t.task_id,"field_id":t.field_id,"activity":t.activity,"planned_date":t.planned_date.isoformat(),"workers":t.required_workers,"duration_hours":t.duration_hours})
    capacity={day.isoformat():n for day,n in worker_capacity.items()}
    conflicts=[{"date":day.isoformat(),"workers_required":n,"workers_available":worker_capacity.get(day,0)} for day,n in by_day.items() if n>worker_capacity.get(day,0)]
    return {"tasks":rows,"daily_worker_capacity":capacity,"capacity_conflicts":conflicts,"schedule_published":False,"human_approval_required":True}
