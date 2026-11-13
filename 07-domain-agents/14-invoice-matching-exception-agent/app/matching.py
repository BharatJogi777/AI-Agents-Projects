"""Compare invoice and PO data; never approve or pay an invoice."""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

@dataclass(frozen=True)
class MatchResult:
    matched: bool
    exceptions: tuple[str,...]
    amount_difference: Decimal

def match_invoice(invoice: dict, purchase_order: dict, *, tolerance: Decimal=Decimal("0.01")) -> MatchResult:
    if not isinstance(invoice,dict) or not isinstance(purchase_order,dict): raise TypeError("invoice and purchase_order must be objects")
    try:
        ia=Decimal(str(invoice["amount"])); pa=Decimal(str(purchase_order["amount"])); tol=Decimal(str(tolerance))
    except (KeyError,InvalidOperation,ValueError): raise ValueError("valid invoice, PO amounts and tolerance are required")
    if not ia.is_finite() or not pa.is_finite() or not tol.is_finite() or ia<0 or pa<0 or tol<0: raise ValueError("amounts and tolerance must be finite and non-negative")
    exceptions=[]
    for key,label in (("vendor_id","vendor"),("currency","currency"),("purchase_order_id","purchase order reference")):
        if not invoice.get(key) or not purchase_order.get(key): exceptions.append(f"Missing {label} on one or both records.")
        elif str(invoice[key]).casefold()!=str(purchase_order[key]).casefold(): exceptions.append(f"{label.title()} does not match.")
    diff=ia-pa
    if abs(diff)>tol: exceptions.append(f"Amount variance {diff} exceeds tolerance {tol}.")
    return MatchResult(not exceptions,tuple(exceptions),diff)
