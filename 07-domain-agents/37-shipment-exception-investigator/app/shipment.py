from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True)
class Shipment:
    shipment_id: str
    expected_at: datetime
    actual_at: datetime | None
    status: str
    last_event_ref: str
def investigate(shipments: list[Shipment], as_of: datetime) -> dict:
    seen=set(); rows=[]; allowed={"in_transit","delivered","delayed","exception","cancelled"}
    for s in shipments:
        if not s.shipment_id.strip() or not s.last_event_ref.strip(): raise ValueError("shipment_id and event reference are required")
        if s.shipment_id in seen: raise ValueError(f"duplicate shipment: {s.shipment_id}")
        if s.status not in allowed: raise ValueError("unsupported shipment status")
        seen.add(s.shipment_id)
        delay=None if s.actual_at is None else int((s.actual_at-s.expected_at).total_seconds()//60)
        overdue=s.actual_at is None and s.expected_at<as_of
        flag="delivered_late" if delay is not None and delay>0 else ("overdue" if overdue else ("exception" if s.status=="exception" else "normal"))
        rows.append({"shipment_id":s.shipment_id,"status":s.status,"delay_minutes":delay,"exception":flag,"evidence_ref":s.last_event_ref,"human_follow_up":flag!="normal"})
    return {"shipments":rows,"exceptions":sum(x["exception"]!="normal" for x in rows),"carrier_contacted":False}
