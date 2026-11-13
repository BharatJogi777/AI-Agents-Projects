import pytest
from app.search import Document,DocumentSearch

def test_search_filters_before_ranking():
    service=DocumentSearch([
        Document("a","Payment guide","payment refund payment",frozenset({"alice"})),
        Document("b","Payment secret","payment token payment",frozenset({"bob"})),
    ])
    results=service.search("payment",principal="alice")
    assert [x["document_id"] for x in results]==["a"]

def test_requires_identity_query_and_bounded_limit():
    service=DocumentSearch([Document("a","Title","body",frozenset({"u"}))],max_results=2)
    with pytest.raises(ValueError): service.search("",principal="u")
    with pytest.raises(ValueError): service.search("body",principal="u",limit=3)
