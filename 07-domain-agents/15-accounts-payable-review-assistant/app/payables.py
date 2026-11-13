"""Pre-payment AP review checklist; no payment initiation or approval."""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

@dataclass(frozen=True)
class PayableReview:
    status: str
    issues: tuple[str,...]
    required_approvals: int

def review_payable(record: dict, *, approval_thresholds: tuple[Decimal,...]=(Decimal("1000"),Decimal("10000"))) -> PayableReview:
    if not isinstance(record,dict): raise TypeError("record must be an object")
    try: amount=Decimal(str(record["amount"]))
    except (KeyError,InvalidOperation,ValueError): raise ValueError("valid amount is required")
    if not amount.is_finite() or amount<0: raise ValueError("amount must be finite and non-negative")
    if not isinstance(approval_thresholds,tuple) or any(not Decimal(str(x)).is_finite() for x in approval_thresholds): raise ValueError("approval_thresholds must be a tuple of finite values")
    thresholds=tuple(Decimal(str(x)) for x in approval_thresholds)
    if any(x<0 for x in thresholds) or tuple(sorted(thresholds))!=thresholds: raise ValueError("approval thresholds must be non-negative and ascending")
    issues=[]
    for field in ("vendor_id","invoice_number","invoice_date","currency","purchase_order_id"):
        if not record.get(field): issues.append(f"Missing {field}.")
    if record.get("duplicate_suspected") is True: issues.append("Possible duplicate invoice; verify before processing.")
    if record.get("match_confirmed") is not True: issues.append("Invoice-to-PO match is not confirmed.")
    if record.get("tax_reviewed") is not True: issues.append("Tax review is not confirmed.")
    approvals=1+sum(amount>threshold for threshold in thresholds)
    status="hold" if issues else "ready_for_approval"
    return PayableReview(status,tuple(issues),approvals)
