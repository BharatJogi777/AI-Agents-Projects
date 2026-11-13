import pytest
from app.compare import Offer,compare_offers
def test_sorts_by_price():
 rows=[Offer("B","item",12,"USD","in stock"),Offer("A","item",8,"USD","limited")]
 assert [x["site"] for x in compare_offers(rows)]==["A","B"]
def test_rejects_mixed_currencies():
 with pytest.raises(ValueError): compare_offers([Offer("A","item",8,"USD","yes"),Offer("B","item",7,"EUR","yes")])
def test_rejects_negative_price():
 with pytest.raises(ValueError): compare_offers([Offer("A","item",-1,"USD","yes")])
