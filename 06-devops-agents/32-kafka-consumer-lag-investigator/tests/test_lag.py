from app.lag import investigate_lag
import pytest

def test_detects_critical_lag():
    out=investigate_lag([{"group":"billing","topic":"payments","partition":0,"lag":15000}])
    assert out[0].severity=="critical"

def test_rejects_duplicate_partition():
    r={"group":"g","topic":"t","partition":0,"lag":2}
    with pytest.raises(ValueError): investigate_lag([r,r])
