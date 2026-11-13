from app.posture import assess_posture
import pytest

def test_prioritizes_critical_controls():
    result = assess_posture([{"id":"bucket-a","controls":{"storage_public":True,"encryption_disabled":True}}])
    assert [x.severity for x in result] == ["critical", "high"]

def test_rejects_non_boolean_control():
    with pytest.raises(ValueError): assess_posture([{"id":"x","controls":{"mfa_disabled":"yes"}}])
