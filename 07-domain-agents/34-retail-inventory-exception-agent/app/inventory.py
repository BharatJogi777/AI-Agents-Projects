from dataclasses import dataclass
@dataclass(frozen=True)
class StockRecord:
    sku: str
    on_hand: int
    reserved: int
    reorder_point: int
    target_stock: int
def detect_exceptions(records: list[StockRecord]) -> dict:
    seen=set(); rows=[]
    for r in records:
        if not r.sku.strip(): raise ValueError("sku is required")
        if r.sku in seen: raise ValueError(f"duplicate sku: {r.sku}")
        seen.add(r.sku)
        if min(r.on_hand,r.reserved,r.reorder_point,r.target_stock)<0 or r.reserved>r.on_hand: raise ValueError("invalid stock quantities")
        available=r.on_hand-r.reserved
        status="reorder" if available<=r.reorder_point else ("overstock" if r.on_hand>r.target_stock else "normal")
        rows.append({"sku":r.sku,"available":available,"status":status,"suggested_replenishment":max(0,r.target_stock-r.on_hand) if status=="reorder" else 0})
    return {"items":rows,"exceptions":sum(x["status"]!="normal" for x in rows),"inventory_mutated":False}
