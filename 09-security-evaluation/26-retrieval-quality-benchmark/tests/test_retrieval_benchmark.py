import pytest
from app.retrieval_benchmark import evaluate_retrieval

def test_ranked_metrics():
    m=evaluate_retrieval(["a","b","c"],{"b","c"},k=2)
    assert (m.precision_at_k,m.recall_at_k,m.reciprocal_rank)==(0.5,0.5,0.5)

def test_no_relevant_results():
    assert evaluate_retrieval(["x"],{"a"},k=1).reciprocal_rank == 0

def test_empty_relevance_set():
    assert evaluate_retrieval(["x"],set(),k=2).recall_at_k == 0

def test_duplicate_ranked_ids_rejected():
    with pytest.raises(ValueError): evaluate_retrieval(["a","a"],{"a"},k=2)
