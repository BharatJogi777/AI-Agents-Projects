from app.payables import review_payable
import pytest

def test_flags_duplicate_and_missing_controls():
    result=review_payable({"amount":"2500","duplicate_suspected":True})
    assert result.status=="hold" and result.required_approvals==2 and result.issues

def test_ready_record_still_requires_approval():
    record={"amount":"100","vendor_id":"v1","invoice_number":"i1","invoice_date":"2026-01-01","currency":"INR","purchase_order_id":"po1","match_confirmed":True,"tax_reviewed":True}
    result=review_payable(record)
    assert result.status=="ready_for_approval" and result.required_approvals==1
