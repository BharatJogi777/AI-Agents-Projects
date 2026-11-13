from app.readiness import review_readiness, REQUIRED
import pytest

def test_reports_missing_rollback_control():
    checks={k:True for k in REQUIRED}; checks["rollback_tested"]=False
    result=review_readiness(checks)
    assert result.status=="not_ready" and "rollback_tested" in result.missing

def test_rejects_unknown_control():
    with pytest.raises(ValueError): review_readiness({"magic":True})
