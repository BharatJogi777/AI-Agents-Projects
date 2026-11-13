"""Evaluate refund eligibility; does not authorize or execute a payment."""
from dataclasses import dataclass

@dataclass(frozen=True)
class RefundDecision:
    eligible_for_review: bool
    reasons: tuple[str,...]
    requires_human_approval: bool=True

def check_refund_eligibility(*, days_since_delivery: int, refund_window_days: int=30, item_condition: str="unused", final_sale: bool=False, proof_of_purchase: bool=True) -> RefundDecision:
    if any(isinstance(v,bool) or not isinstance(v,int) for v in (days_since_delivery,refund_window_days)) or days_since_delivery<0 or refund_window_days<0: raise ValueError("day values must be non-negative integers")
    if item_condition not in {"unused","opened","damaged","used"}: raise ValueError("unsupported item_condition")
    if any(not isinstance(v,bool) for v in (final_sale,proof_of_purchase)): raise ValueError("policy flags must be booleans")
    reasons=[]
    if final_sale: reasons.append("Item is marked final sale.")
    if not proof_of_purchase: reasons.append("Proof of purchase was not supplied.")
    if days_since_delivery>refund_window_days: reasons.append("Refund request is outside the configured window.")
    if item_condition=="used": reasons.append("Used items require a separate exception review.")
    eligible=not reasons
    if eligible: reasons.append("Supplied details meet the configured screening rules; final approval remains with an authorized agent.")
    return RefundDecision(eligible,tuple(reasons))
