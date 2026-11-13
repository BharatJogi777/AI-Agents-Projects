from app.vpc_diagnosis import diagnose_path
import pytest

def test_identifies_blocked_component():
    path = {k: {"reachable": True} for k in ("route", "security_group", "network_acl", "endpoint")}
    path["route"] = {"reachable": False, "evidence": "No matching route"}
    result = diagnose_path(path)
    assert result[0].status == "blocked"

def test_rejects_missing_component():
    with pytest.raises(ValueError): diagnose_path({})
