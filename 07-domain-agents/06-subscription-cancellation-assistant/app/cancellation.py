"""Policy-based cancellation assessment; no account mutations."""
from dataclasses import dataclass

@dataclass(frozen=True)
class CancellationAssessment:
    can_submit_request: bool
    required_actions: tuple[str,...]
    warnings: tuple[str,...]

def assess_cancellation(*, subscription_id: str, status: str, billing_state: str, requested_end: str="period_end", outstanding_balance: bool=False, minimum_term_complete: bool=True) -> CancellationAssessment:
    if not isinstance(subscription_id,str) or not subscription_id.strip(): raise ValueError("subscription_id is required")
    if status not in {"trial","active","past_due","paused","cancelled"}: raise ValueError("invalid subscription status")
    if billing_state not in {"current","past_due","unknown"}: raise ValueError("invalid billing_state")
    if requested_end not in {"immediate","period_end"}: raise ValueError("requested_end must be immediate or period_end")
    if any(not isinstance(x,bool) for x in (outstanding_balance,minimum_term_complete)): raise ValueError("flags must be booleans")
    actions=[]; warnings=[]
    if status=="cancelled": warnings.append("Subscription is already cancelled.")
    elif status=="paused": warnings.append("Confirm whether paused subscriptions are eligible under the applicable policy.")
    else: actions.append(f"Submit a cancellation request for {subscription_id.strip()} with requested effective time: {requested_end}.")
    if outstanding_balance or billing_state=="past_due": actions.append("Route outstanding billing to the billing team; cancellation does not waive balances.")
    if billing_state=="unknown": warnings.append("Billing state is unknown and must be verified.")
    if not minimum_term_complete: warnings.append("Minimum term may apply; obtain contract review before confirming the effective date.")
    actions.append("Send customer confirmation only after the subscription system acknowledges the request.")
    return CancellationAssessment(status!="cancelled" and billing_state!="unknown",tuple(actions),tuple(warnings))
