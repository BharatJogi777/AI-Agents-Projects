from app.error_budget import calculate_budget
import pytest

def test_reports_exhausted_budget():
    result=calculate_budget(1000,2,target_slo=.999)
    assert result.status=="exhausted"

def test_rejects_invalid_slo():
    with pytest.raises(ValueError): calculate_budget(100,1,target_slo=1)
