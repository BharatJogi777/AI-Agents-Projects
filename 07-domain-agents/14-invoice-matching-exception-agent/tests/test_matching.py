from app.matching import match_invoice
import pytest

def test_matches_equal_records():
    record={"vendor_id":"v1","currency":"INR","purchase_order_id":"po1","amount":"125.00"}
    result=match_invoice(record,record)
    assert result.matched and result.amount_difference==0

def test_flags_vendor_and_amount_mismatch():
    a={"vendor_id":"v1","currency":"INR","purchase_order_id":"po1","amount":"150"}
    b={"vendor_id":"v2","currency":"INR","purchase_order_id":"po1","amount":"100"}
    assert not match_invoice(a,b).matched
