import pytest
from app.deployment_readiness import Gate,assess_readiness
def test_missing_evidence_blocks_release():
 r=assess_readiness([Gate("tests",True,"run-123"),Gate("security",True)],required_gates={"tests","security","privacy"})
 assert not r.ready and r.blockers==("privacy","security") and r.missing_evidence==("privacy","security")
def test_ready_when_all_gates_pass_with_evidence():
 r=assess_readiness([Gate("tests",True,"ci/1"),Gate("security",True,"scan/2")],required_gates={"tests","security"})
 assert r.ready and r.passed==2
