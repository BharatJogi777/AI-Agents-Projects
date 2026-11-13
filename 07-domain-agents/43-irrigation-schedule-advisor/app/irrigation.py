from dataclasses import dataclass
@dataclass(frozen=True)
class FieldWaterStatus:
    field_id: str
    area_hectares: float
    soil_moisture_pct: float
    target_moisture_pct: float
    application_rate_mm_per_hour: float
def advise_irrigation(fields: list[FieldWaterStatus], max_hours_per_field: float=8) -> dict:
    if max_hours_per_field<=0: raise ValueError("max_hours_per_field must be positive")
    seen=set(); rows=[]
    for f in fields:
        if not f.field_id.strip() or f.field_id in seen: raise ValueError("field ids must be non-empty and unique")
        if f.area_hectares<=0 or f.application_rate_mm_per_hour<=0: raise ValueError("area and application rate must be positive")
        if not 0<=f.soil_moisture_pct<=100 or not 0<=f.target_moisture_pct<=100: raise ValueError("moisture percentages must be between 0 and 100")
        seen.add(f.field_id); deficit=max(0,f.target_moisture_pct-f.soil_moisture_pct)
        hours=min(max_hours_per_field,deficit/f.application_rate_mm_per_hour)
        rows.append({"field_id":f.field_id,"moisture_deficit_pct":round(deficit,2),"suggested_runtime_hours":round(hours,2),"capped":deficit/f.application_rate_mm_per_hour>max_hours_per_field,"advice":"review soil and weather conditions before irrigation" if deficit else "no irrigation indicated by supplied moisture values"})
    return {"fields":rows,"water_volume_estimated":False,"irrigation_started":False,"agronomist_review_required":True}
