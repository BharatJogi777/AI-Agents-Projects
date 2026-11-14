import pytest
from app.citation_network import analyze_citations
def test_graph_edges_orphans_and_unknowns():
 r=analyze_citations(papers=["A","B","C"],citations={"A":["B","X"]})
 assert r.edges==(("A","B"),) and r.unknown_references==(("A","X"),)
 assert r.orphan_nodes==("C",)
def test_rejects_duplicate_ids():
 with pytest.raises(ValueError): analyze_citations(papers=["A","A"],citations={})
