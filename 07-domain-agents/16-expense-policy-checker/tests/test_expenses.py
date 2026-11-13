from app.expenses import check_expense
import pytest

def test_flags_missing_receipt_and_limit_breach():
    result=check_expense({"category":"travel","amount":"150","business_purpose":"Client visit","currency":"INR"},category_limits={"travel":"100"})
    assert not result.eligible_for_review and len(result.issues)==2

def test_rejects_unknown_category():
    with pytest.raises(ValueError): check_expense({"category":"other","amount":"1"},category_limits={})
