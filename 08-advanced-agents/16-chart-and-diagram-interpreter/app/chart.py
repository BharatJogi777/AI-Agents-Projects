"""Validate extracted chart data and compute conservative summaries."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Datum:
    label:str
    value:float
def interpret_chart(title:str,unit:str,data:list[Datum])->dict:
    if not title.strip() or not unit.strip() or not data: raise ValueError("title, unit, and chart data are required")
    if any(not d.label.strip() for d in data): raise ValueError("every datum needs a label")
    if len({d.label for d in data})!=len(data): raise ValueError("labels must be unique")
    values=[d.value for d in data]
    return {"title":title,"unit":unit,"points":[d.__dict__ for d in data],
            "minimum":{"label":data[values.index(min(values))].label,"value":min(values)},
            "maximum":{"label":data[values.index(max(values))].label,"value":max(values)},
            "total":sum(values),"interpretation":"Computed only from supplied values; axis scale and source accuracy were not independently verified."}
