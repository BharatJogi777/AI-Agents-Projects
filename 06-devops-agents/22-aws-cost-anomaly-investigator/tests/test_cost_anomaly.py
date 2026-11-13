from app.cost_anomaly import investigate_costs
import pytest

def test_finds_large_increase():
    result = investigate_costs({"EC2":100}, {"EC2":160})
    assert result[0].increase_percent == 60

def test_rejects_negative_cost():
    with pytest.raises(ValueError): investigate_costs({}, {"S3":-1})
