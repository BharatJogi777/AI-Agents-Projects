from app.refund import check_refund_eligibility
import pytest

def test_rejects_out_of_window_request():
    result=check_refund_eligibility(days_since_delivery=45,refund_window_days=30)
    assert not result.eligible_for_review

def test_rejects_negative_age():
    with pytest.raises(ValueError): check_refund_eligibility(days_since_delivery=-1)
