"""Prepare a return workflow checklist; no label or refund is generated."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ReturnPlan:
    case_id: str
    steps: tuple[str,...]
    blocked: bool
    requires_agent_approval: bool=True

def plan_return(case_id: str, *, delivered: bool, return_reason: str, item_category: str, hazardous: bool=False, original_packaging_available: bool=True) -> ReturnPlan:
    if not isinstance(case_id,str) or not case_id.strip(): raise ValueError("case_id is required")
    if any(not isinstance(v,bool) for v in (delivered,hazardous,original_packaging_available)): raise ValueError("workflow flags must be booleans")
    if not isinstance(return_reason,str) or not return_reason.strip() or not isinstance(item_category,str) or not item_category.strip(): raise ValueError("return_reason and item_category are required")
    steps=[]; blocked=False
    if not delivered: blocked=True; steps.append("Wait for delivery confirmation or ask an agent to investigate the shipment.")
    else: steps.append("Verify order identity, delivery date, and return-window policy.")
    steps.append(f"Record customer-provided return reason: {return_reason.strip()}.")
    steps.append(f"Check category-specific return restrictions for: {item_category.strip()}.")
    if hazardous: blocked=True; steps.append("Stop standard parcel workflow; obtain specialist handling guidance for hazardous goods.")
    if not original_packaging_available: steps.append("Confirm approved alternative packaging instructions with the returns team.")
    else: steps.append("Ask customer to retain original packaging where policy permits.")
    steps.extend(["Obtain authorized return approval before issuing a label.","After receipt, inspect item and record disposition.","Process any refund or exchange only through the authorized payment workflow."])
    return ReturnPlan(case_id.strip(),tuple(steps),blocked)
