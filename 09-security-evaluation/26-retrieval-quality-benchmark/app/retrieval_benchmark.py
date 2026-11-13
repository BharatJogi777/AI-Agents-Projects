"""Evaluate ranked retrieval results against relevance judgments."""
from dataclasses import dataclass

@dataclass(frozen=True)
class RetrievalMetrics:
    precision_at_k: float
    recall_at_k: float
    reciprocal_rank: float
    relevant_found: int

def evaluate_retrieval(ranked_ids: list[str], relevant_ids: set[str], *, k: int) -> RetrievalMetrics:
    if not isinstance(k,int) or isinstance(k,bool) or k < 1: raise ValueError("k must be a positive integer")
    if any(not isinstance(x,str) or not x for x in ranked_ids) or any(not isinstance(x,str) or not x for x in relevant_ids):
        raise ValueError("document IDs must be non-empty strings")
    if len(set(ranked_ids)) != len(ranked_ids): raise ValueError("ranked_ids must not contain duplicates")
    top=ranked_ids[:k]; found=sum(x in relevant_ids for x in top)
    first=next((i for i,x in enumerate(top,1) if x in relevant_ids),None)
    return RetrievalMetrics(found/k, found/len(relevant_ids) if relevant_ids else 0.0, 1/first if first else 0.0, found)
