from dataclasses import dataclass
from datetime import date
@dataclass(frozen=True)
class Vehicle:
    vehicle_id: str
    odometer_km: int
    last_service_km: int
    interval_km: int
    last_service_date: date
    interval_days: int
def assess_maintenance(vehicles: list[Vehicle], as_of: date | None = None) -> dict:
    as_of=as_of or date.today(); seen=set(); rows=[]
    for v in vehicles:
        if not v.vehicle_id.strip() or v.vehicle_id in seen: raise ValueError("vehicle ids must be non-empty and unique")
        if min(v.odometer_km,v.last_service_km)<0 or v.odometer_km<v.last_service_km or v.interval_km<=0 or v.interval_days<=0: raise ValueError("invalid odometer or service interval")
        if v.last_service_date>as_of: raise ValueError("last service date cannot be in the future")
        seen.add(v.vehicle_id); km_due=v.odometer_km-v.last_service_km>=v.interval_km; date_due=(as_of-v.last_service_date).days>=v.interval_days
        rows.append({"vehicle_id":v.vehicle_id,"distance_due":km_due,"time_due":date_due,"maintenance_due":km_due or date_due,"km_until_due":max(0,v.interval_km-(v.odometer_km-v.last_service_km))})
    return {"vehicles":rows,"due_count":sum(x["maintenance_due"] for x in rows),"work_order_created":False}
