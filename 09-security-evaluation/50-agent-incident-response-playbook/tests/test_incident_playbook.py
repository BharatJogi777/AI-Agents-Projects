import pytest
from app.incident_playbook import create_incident_plan
def test_security_incident_plan_escalates():
 p=create_incident_plan("data_exposure",severity="critical")
 assert p.escalation_required and "preserve access and audit logs" in p.actions
def test_unknown_category_and_severity_rejected():
 with pytest.raises(ValueError): create_incident_plan("unknown",severity="low")
 with pytest.raises(ValueError): create_incident_plan("tool_misuse",severity="urgent")
