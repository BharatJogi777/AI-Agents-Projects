import pytest
from app.capacity import plan_capacity

def test_calculates_nodes_from_limiting_resource():
    result=plan_capacity([{"cpu_millicores":1500,"memory_mib":3000}],{"cpu_millicores":1000,"memory_mib":4096},reserve=0)
    assert result["nodes_required"] == 2
    assert result["limiting_resource"] == "cpu"

def test_rejects_zero_capacity():
    with pytest.raises(ValueError): plan_capacity([],{"cpu_millicores":0,"memory_mib":10})
