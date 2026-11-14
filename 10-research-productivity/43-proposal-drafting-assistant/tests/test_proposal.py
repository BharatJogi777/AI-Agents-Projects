from app.proposal import ProposalInput,draft_proposal
import pytest
def test_draft():
 r=draft_proposal(ProposalInput("Acme","Improve onboarding",("Audit",),("Report",),("Discovery",)))
 assert r["status"].startswith("Draft") and r["deliverables"]==["Report"]
def test_empty_scope_rejected():
 with pytest.raises(ValueError,match="scope"): draft_proposal(ProposalInput("Acme","Goal",(),("D",),("M",)))
def test_missing_client_rejected():
 with pytest.raises(ValueError): draft_proposal(ProposalInput(" ","Goal",("S",),("D",),("M",)))
