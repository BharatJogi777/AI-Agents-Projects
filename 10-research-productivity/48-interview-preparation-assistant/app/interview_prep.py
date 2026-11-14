"""Create an interview practice plan from explicitly supplied inputs."""
from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True)
class Competency:
    name:str; confidence:int; importance:int
def build_practice_plan(competencies:list[Competency],interview_date:date,today:date)->dict:
    if not competencies: raise ValueError("at least one competency is required")
    if interview_date<today: raise ValueError("interview_date cannot be in the past")
    names=set(); ranked=[]
    for item in competencies:
        key=item.name.casefold().strip()
        if not key or key in names: raise ValueError("competency names must be non-empty and unique")
        names.add(key)
        if not 1<=item.confidence<=5 or not 1<=item.importance<=5: raise ValueError("confidence and importance must be between 1 and 5")
        gap=item.importance-item.confidence
        ranked.append({"competency":item.name,"confidence":item.confidence,"importance":item.importance,"practice_priority":max(0,gap)*item.importance})
    ranked.sort(key=lambda x:(-x["practice_priority"],x["competency"].casefold()))
    return {"days_until_interview":(interview_date-today).days,"practice_items":ranked,"review_required":True}
