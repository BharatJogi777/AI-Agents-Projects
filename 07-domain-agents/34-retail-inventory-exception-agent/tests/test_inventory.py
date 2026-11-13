import pytest
from app.inventory import StockRecord,detect_exceptions
def test_detects_reorder():
 r=detect_exceptions([StockRecord("SKU1",5,2,4,20)])
 assert r["items"][0]["status"]=="reorder" and r["items"][0]["suggested_replenishment"]==15
def test_rejects_reserved_above_on_hand():
 with pytest.raises(ValueError): detect_exceptions([StockRecord("SKU",2,3,1,5)])
