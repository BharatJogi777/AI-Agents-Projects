from app.rfp import Requirement,Evidence,map_rfp
import pytest
def test_maps_and_flags_gaps():
 r=map_rfp([Requirement("1","Security?"),Requirement("2","Support?")],[Evidence("1","SOC report","security.pdf")])
 assert r["responses"][0]["status"]=="needs_review" and r["unanswered_count"]==1 and r["approval_required"]
def test_unknown_evidence_rejected():
 with pytest.raises(ValueError,match="unknown"): map_rfp([Requirement("1","Q")],[Evidence("2","Text","source")])
def test_duplicate_requirements_rejected():
 with pytest.raises(ValueError): map_rfp([Requirement("1","A"),Requirement("1","B")],[])
