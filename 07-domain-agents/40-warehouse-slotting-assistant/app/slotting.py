from dataclasses import dataclass
@dataclass(frozen=True)
class SKU:
    sku: str
    picks_per_day: float
    current_zone: str
    available_locations: tuple[str,...]
def recommend_slots(items: list[SKU], zone_capacity: dict[str,int]) -> dict:
    seen=set(); counts={z:0 for z in zone_capacity}; rows=[]
    if any(not z.strip() or cap<0 for z,cap in zone_capacity.items()): raise ValueError("zone names and capacities must be valid")
    for item in items:
        if not item.sku.strip() or item.sku in seen: raise ValueError("SKU values must be non-empty and unique")
        if item.picks_per_day<0: raise ValueError("pick frequency cannot be negative")
        if not item.available_locations: raise ValueError("SKU needs at least one available location")
        seen.add(item.sku)
    for item in sorted(items,key=lambda x:(-x.picks_per_day,x.sku)):
        candidates=[z for z in item.available_locations if z in counts and counts[z]<zone_capacity[z]]
        candidates.sort(key=lambda z:(0 if z==item.current_zone else 1,z))
        chosen=candidates[0] if candidates else None
        if chosen: counts[chosen]+=1
        rows.append({"sku":item.sku,"recommended_zone":chosen,"current_zone":item.current_zone,"needs_manual_slot":chosen is None})
    return {"recommendations":rows,"zone_usage":counts,"inventory_relocated":False}
