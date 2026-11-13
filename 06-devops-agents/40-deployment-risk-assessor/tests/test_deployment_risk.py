from app.deployment_risk import assess_deployment
import pytest

def test_flags_untested_risky_release():
    result=assess_deployment("large",tests_passed=False,rollback_tested=False,database_migration=True,backward_compatible=False,critical_service=True,canary_available=False)
    assert result.level=="critical"

def test_rejects_unknown_change_size():
    with pytest.raises(ValueError): assess_deployment("huge",tests_passed=True,rollback_tested=True)
