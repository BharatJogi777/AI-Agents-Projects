"""Format order status from a supplied record; no live order lookup occurs."""
from dataclasses import dataclass

_ALLOWED={"created","confirmed","processing","packed","shipped","out_for_delivery","delivered","cancelled","on_hold"}
@dataclass(frozen=True)
class OrderSummary:
    order_id: str
    status: str
    customer_message: str
    tracking_reference: str | None

def get_order_status(record: dict) -> OrderSummary:
    if not isinstance(record,dict): raise TypeError("record must be an object")
    oid=record.get("order_id"); status=record.get("status"); tracking=record.get("tracking_reference")
    if not isinstance(oid,str) or not oid.strip(): raise ValueError("order_id is required")
    if status not in _ALLOWED: raise ValueError(f"status must be one of {sorted(_ALLOWED)}")
    if tracking is not None and (not isinstance(tracking,str) or not tracking.strip()): raise ValueError("tracking_reference must be non-empty when provided")
    messages={"created":"Your order has been created and is awaiting confirmation.","confirmed":"Your order is confirmed.","processing":"Your order is being prepared.","packed":"Your order has been packed.","shipped":"Your order has shipped.","out_for_delivery":"Your order is out for delivery.","delivered":"Your order is marked as delivered.","cancelled":"Your order has been cancelled.","on_hold":"Your order is on hold; support review may be needed."}
    if status in {"shipped","out_for_delivery"} and tracking: messages[status]+=" Tracking reference: "+tracking
    return OrderSummary(oid.strip(),status,messages[status],tracking)
