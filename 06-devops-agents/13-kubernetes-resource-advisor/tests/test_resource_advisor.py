import pytest
from app.resource_advisor import advise_resources

def test_recommends_headroom():
    rows=[{"namespace":"prod","pod":"api-1","container":"api","cpu_millicores":100,"memory_mib":200,"cpu_request_millicores":200,"memory_request_mib":400}]
    result=advise_resources(rows)
    assert result[0]["suggested_cpu_request_millicores"] == 125
    assert result[0]["suggested_memory_request_mib"] == 250

def test_rejects_invalid_headroom():
    with pytest.raises(ValueError): advise_resources([], 3)
