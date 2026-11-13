import pytest
from app.negotiation import negotiate

def test_agreement_when_reservation_ranges_overlap():
    result=negotiate({"buyer":(100,80),"seller":(60,90)})
    assert result.agreement and 60 <= result.amount <= 100

def test_no_overlap_and_invalid_rounds():
    assert not negotiate({"buyer":(50,40),"seller":(70,80)}).agreement
    with pytest.raises(ValueError): negotiate({"buyer":(1,1),"seller":(0,0)},0)
