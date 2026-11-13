"""State machine for human takeover; does not control a browser."""
from dataclasses import dataclass

@dataclass(frozen=True)
class HandoffState:
    workflow_id: str
    status: str
    reason: str
    audit: tuple[str, ...]

def request_takeover(state: HandoffState, *, reason: str) -> HandoffState:
    if state.status not in {"automating","paused"}:
        raise ValueError("takeover can only be requested from an active workflow")
    if not reason.strip():
        raise ValueError("takeover reason is required")
    return HandoffState(state.workflow_id,"awaiting_human",reason,state.audit+("takeover_requested",))

def resolve_takeover(state: HandoffState, *, decision: str, operator_id: str) -> HandoffState:
    if state.status != "awaiting_human":
        raise ValueError("workflow is not awaiting human input")
    if decision not in {"resume","cancel"}:
        raise ValueError("decision must be resume or cancel")
    if not operator_id.strip():
        raise ValueError("operator_id is required")
    status = "automating" if decision == "resume" else "cancelled"
    return HandoffState(state.workflow_id,status,state.reason,state.audit+(f"human_{decision}:{operator_id}",))

def initial_state(workflow_id: str) -> HandoffState:
    if not workflow_id.strip():
        raise ValueError("workflow_id is required")
    return HandoffState(workflow_id,"automating","",())
