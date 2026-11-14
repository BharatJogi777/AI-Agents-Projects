"""Produce incident response checklists; never execute response actions."""
from dataclasses import dataclass
@dataclass(frozen=True)
class IncidentPlan:
 category:str; severity:str; actions:tuple[str,...]; escalation_required:bool
_PLAYBOOK={
 "prompt_injection":("isolate affected session","preserve prompt and tool-call evidence","review retrieved and external content","rotate exposed credentials if indicated"),
 "data_exposure":("restrict affected data access","preserve access and audit logs","identify affected records and principals","notify privacy and security owners"),
 "tool_misuse":("disable affected tool permission","preserve tool arguments and results","review authorization and approval checks","validate downstream side effects"),
 "service_outage":("check service health and dependency status","preserve traces and error samples","activate documented fallback if approved","communicate service impact"),
}
def create_incident_plan(category:str,*,severity:str)->IncidentPlan:
 if category not in _PLAYBOOK: raise ValueError("unsupported incident category")
 if severity not in {"low","medium","high","critical"}: raise ValueError("invalid severity")
 return IncidentPlan(category,severity,_PLAYBOOK[category],severity in {"high","critical"})
