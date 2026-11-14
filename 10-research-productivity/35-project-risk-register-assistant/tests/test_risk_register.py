import pytest
from app.risk_register import build_risk_register

def test_ranks_highest_scoring_risk_first():
    r=build_risk_register(risks=[{"id":"a","description":"Delay","likelihood":2,"impact":2},{"id":"b","description":"Outage","likelihood":5,"impact":5}])
    assert r[0].risk_id=="b" and r[0].priority=="critical"

def test_rejects_out_of_range_rating():
    with pytest.raises(ValueError):
        build_risk_register(risks=[{"id":"x","description":"Risk","likelihood":0,"impact":3}])
