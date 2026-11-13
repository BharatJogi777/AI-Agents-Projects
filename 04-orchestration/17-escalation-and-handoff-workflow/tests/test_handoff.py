import pytest
from app.handoff import EscalationWorkflow

def test_escalates_and_records_handoff():
    sent = []
    flow = EscalationWorkflow(["worker", "lead", "manager"], sent.append)
    record = flow.escalate("job-1", 0, "blocked")
    assert record.to_owner == "lead" and sent == [record] and flow.history == [record]

def test_escalation_limit():
    flow = EscalationWorkflow(["worker", "lead"], lambda record: None)
    with pytest.raises(RuntimeError): flow.escalate("job", 1, "still blocked")

def test_invalid_reason_rejected():
    flow = EscalationWorkflow(["worker", "lead"], lambda record: None)
    with pytest.raises(ValueError): flow.escalate("job", 0, " ")
