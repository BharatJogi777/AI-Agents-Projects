import pytest
from app.knowledge_graph import curate_graph

def test_finds_duplicate_dangling_and_self_loop():
    report = curate_graph(entities=["A", "B", "A"], relationships=[("A","knows","B"),("B","loops","B"),("X","refers","A")])
    assert report.duplicate_entities == ("A",)
    assert len(report.dangling_relationships) == 1
    assert len(report.self_loops) == 1

def test_rejects_malformed_edge():
    with pytest.raises(ValueError):
        curate_graph(entities=["A"], relationships=[("A","related")])
