from app.cost import plan_cost_optimizations
import pytest

def test_flags_idle_resource():
    result=plan_cost_optimizations([{"resource_id":"vm-1","monthly_cost":100,"average_utilization_percent":40,"idle_days":30}])
    assert result[0].action=="review_for_decommission" and result[0].estimated_monthly_savings==100

def test_rejects_negative_cost():
    with pytest.raises(ValueError): plan_cost_optimizations([{"resource_id":"x","monthly_cost":-1,"average_utilization_percent":10,"idle_days":0}])
