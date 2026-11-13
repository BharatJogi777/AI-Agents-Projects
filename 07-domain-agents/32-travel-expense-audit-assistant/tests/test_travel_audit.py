from decimal import Decimal
import pytest
from app.travel_audit import TravelExpense,audit_expenses
def test_flags_missing_receipt_and_limit():
 r=audit_expenses([TravelExpense("E1","hotel",Decimal("120"),"usd")],{"hotel":Decimal("100")},{"hotel"})
 assert set(r["expenses"][0]["flags"])=={"over_category_limit","receipt_missing"} and not r["payment_authorized"]
def test_rejects_negative():
 with pytest.raises(ValueError): audit_expenses([TravelExpense("E1","taxi",Decimal("-1"),"USD")],{})
