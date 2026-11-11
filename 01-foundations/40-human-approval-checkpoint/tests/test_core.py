import pytest
from approval_gate import *
def test_approval_one_time_and_payload_bound():
 g=ApprovalGate(lambda:1.);action={"operation":"deploy","environment":"staging"};a=g.request(action)
 assert g.decide(a.id,action,True).status=="approved"
 with pytest.raises(ValueError):g.decide(a.id,action,True)
def test_tampering_expiry_and_non_json_payload():
 now=[1.];g=ApprovalGate(lambda:now[0]);a=g.request({"x":1})
 with pytest.raises(PermissionError):g.decide(a.id,{"x":2},True)
 a=g.request({"x":1},1);now[0]=2
 with pytest.raises(TimeoutError):g.decide(a.id,{"x":1},True)
 assert g.get(a.id).status=="expired"
 with pytest.raises(ValueError):g.request({"bad":object()})
