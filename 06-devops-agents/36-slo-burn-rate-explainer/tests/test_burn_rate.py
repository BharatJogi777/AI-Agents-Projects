from app.burn_rate import explain_burn_rate
import pytest

def test_detects_fast_burn():
    result=explain_burn_rate([{"name":"5m","total_requests":10000,"error_requests":200}],target_slo=.999)
    assert result[0].severity=="critical"

def test_rejects_errors_above_total():
    with pytest.raises(ValueError): explain_burn_rate([{"name":"x","total_requests":10,"error_requests":11}])
