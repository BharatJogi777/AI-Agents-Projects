import pytest
from app import Candidate,multi_query_retrieve
def test_merge():
 def search(q): return [Candidate("a","A",1),Candidate("b","B",.5)] if q=="one" else [Candidate("b","B",.9)]
 r=multi_query_retrieve(["one","two"],search); assert r[0].id=="b" and r[0].matched_queries==(0,1)
def test_empty():
 with pytest.raises(ValueError): multi_query_retrieve([],lambda q:[])
