import pytest
from app.slotting import SKU,recommend_slots
def test_assigns_available_zone():
 r=recommend_slots([SKU("A",20,"bulk",("fast","bulk"))],{"fast":1,"bulk":2})
 assert r["recommendations"][0]["recommended_zone"]=="bulk" and not r["inventory_relocated"]
def test_rejects_duplicate_sku():
 x=SKU("A",2,"z",("z",))
 with pytest.raises(ValueError): recommend_slots([x,x],{"z":2})
