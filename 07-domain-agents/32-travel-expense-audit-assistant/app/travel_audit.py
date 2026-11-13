from dataclasses import dataclass
from decimal import Decimal,InvalidOperation
@dataclass(frozen=True)
class TravelExpense:
    expense_id: str
    category: str
    amount: Decimal
    currency: str
    receipt_ref: str | None = None
def audit_expenses(items: list[TravelExpense], limits: dict[str,Decimal], receipt_required: set[str] | None = None) -> dict:
    seen=set(); results=[]
    for e in items:
        if not e.expense_id.strip() or not e.category.strip() or not e.currency.strip(): raise ValueError("expense id, category and currency are required")
        if e.expense_id in seen: raise ValueError(f"duplicate expense id: {e.expense_id}")
        seen.add(e.expense_id)
        try: amount=Decimal(e.amount)
        except (InvalidOperation,TypeError): raise ValueError("invalid expense amount")
        if not amount.is_finite() or amount<0: raise ValueError("expense amount must be finite and non-negative")
        limit=limits.get(e.category)
        flags=[]
        if limit is None: flags.append("no_policy_limit_configured")
        elif amount>Decimal(limit): flags.append("over_category_limit")
        if e.category in (receipt_required or set()) and not e.receipt_ref: flags.append("receipt_missing")
        results.append({"expense_id":e.expense_id,"amount":str(amount),"currency":e.currency.upper(),"flags":flags,"review_required":bool(flags)})
    return {"expenses":results,"flagged_count":sum(bool(x["flags"]) for x in results),"payment_authorized":False}
