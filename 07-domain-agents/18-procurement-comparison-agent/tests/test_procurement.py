from app.procurement import compare_quotes
import pytest

def test_sorts_quotes_and_keeps_compliance_visible():
    result=compare_quotes([{"vendor_id":"b","total_cost":"200","lead_time_days":3,"compliant":True},{"vendor_id":"a","total_cost":"100","lead_time_days":5,"compliant":None}])
    assert result[0].vendor_id=="a" and result[0].issues

def test_rejects_empty_quotes():
    with pytest.raises(ValueError): compare_quotes([])
