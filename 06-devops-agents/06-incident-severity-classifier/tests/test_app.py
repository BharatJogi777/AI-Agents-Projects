import pytest
from app.severity import IncidentSignals, classify_severity

def test_critical_data_loss_escalates():
    result=classify_severity(IncidentSignals(800,1000,True,True,90,False))
    assert result["severity"] == "SEV1" and result["requires_human_confirmation"]

def test_workaround_reduces_score():
    a=IncidentSignals(200,1000,False,False,20,False)
    b=IncidentSignals(200,1000,False,False,20,True)
    assert classify_severity(b)["score"] < classify_severity(a)["score"]

def test_rejects_invalid_population():
    with pytest.raises(ValueError): classify_severity(IncidentSignals(2,0,False,False,0,False))
