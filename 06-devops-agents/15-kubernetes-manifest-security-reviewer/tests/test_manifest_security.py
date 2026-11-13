import pytest
from app.manifest_security import review_manifests

def test_flags_privileged_and_missing_hardening():
    doc={"kind":"Deployment","metadata":{"name":"api"},"spec":{"template":{"spec":{"containers":[{"name":"api","securityContext":{"privileged":True}}]}}}}
    codes={f["code"] for f in review_manifests([doc])}
    assert {"PRIVILEGED","PRIVILEGE_ESCALATION","SECCOMP_PROFILE"} <= codes

def test_rejects_invalid_document():
    with pytest.raises(ValueError): review_manifests([{}])
