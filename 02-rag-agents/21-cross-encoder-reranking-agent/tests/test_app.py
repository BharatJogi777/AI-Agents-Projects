import pytest
from app import Passage,rerank
def test_rerank_and_deduplicate():
 p=[Passage("a","low",{}),Passage("b","high",{}),Passage("a","duplicate",{})]
 r=rerank("q",p,lambda q,t:{"low":.1,"high":.9}[t]); assert [x.passage.id for x in r]==["b","a"] and r[1].original_rank==1
def test_reject_bad_score():
 with pytest.raises(ValueError): rerank("q",[Passage("a","x",{})],lambda q,t:float("nan"))
