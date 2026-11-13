from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True)
class Goal:
    goal_id: str
    title: str
    target_date: date
    weekly_hours: float
    priority: int
def coach_plan(goals: list[Goal], as_of: date) -> dict:
    seen=set(); rows=[]
    for g in goals:
        if not g.goal_id.strip() or not g.title.strip() or g.goal_id in seen: raise ValueError("goal ids and titles must be non-empty and unique")
        if g.target_date<as_of: raise ValueError("goal target date cannot be in the past")
        if g.weekly_hours<=0 or not 1<=g.priority<=5: raise ValueError("weekly hours must be positive and priority between 1 and 5")
        seen.add(g.goal_id); days=(g.target_date-as_of).days
        rows.append({"goal_id":g.goal_id,"title":g.title,"days_remaining":days,"weekly_hours":g.weekly_hours,"priority":g.priority,"status":"due_soon" if days<=14 else "on_track"})
    rows.sort(key=lambda x:(-x["priority"],x["days_remaining"],x["goal_id"]))
    return {"goals":rows,"total_weekly_hours":round(sum(x["weekly_hours"] for x in rows),2),"plan_is_advisory":True,"completion_claimed":False}
