from app.purchase_order import prepare_purchase_order
import pytest

def test_calculates_line_and_subtotal():
    result=prepare_purchase_order(vendor_id="v1",currency="inr",items=[{"description":"Keyboard","quantity":2,"unit_price":"25.50"}])
    assert result.subtotal==result.lines[0][3] and result.subtotal==51 and result.requires_approval

def test_rejects_non_positive_quantity():
    with pytest.raises(ValueError): prepare_purchase_order(vendor_id="v1",currency="INR",items=[{"description":"x","quantity":0,"unit_price":1}])
