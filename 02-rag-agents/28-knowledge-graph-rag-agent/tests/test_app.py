import pytest
from app import Triple,validate_triples,retrieve_connected
def test_graph_retrieval():
 ts=validate_triples([Triple("A","works_at","B","doc"),Triple("A","works_at","B","doc")],{"works_at"}); assert len(ts)==1 and retrieve_connected("b",ts)[0].subject=="A"
def test_predicate_allowlist():
 with pytest.raises(ValueError): validate_triples([Triple("A","owns","B","d")],{"works_at"})
