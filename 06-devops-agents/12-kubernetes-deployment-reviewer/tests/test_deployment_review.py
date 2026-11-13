import pytest
from app.deployment_review import review_deployment

def test_flags_missing_probes_and_privilege():
    doc={"kind":"Deployment","metadata":{"name":"api"},"spec":{"replicas":1,"template":{"spec":{"containers":[{"name":"api","image":"api:v1","securityContext":{"privileged":True}}]}}}}
    codes={f["code"] for f in review_deployment(doc)}
    assert {"SINGLE_REPLICA","MISSING_READINESS","PRIVILEGED_CONTAINER"} <= codes

def test_rejects_wrong_kind():
    with pytest.raises(ValueError): review_deployment({"kind":"Pod"})
