import pytest
from app.discovery import discover
def test_search_matches_name_and_tags():
 r=discover("wireless keyboard",[{"id":"p1","name":"Keyboard","tags":["wireless"]}])
 assert r["results"][0]["product_id"]=="p1" and not r["purchase_performed"]
def test_rejects_empty_query():
 with pytest.raises(ValueError): discover(" ",[])
