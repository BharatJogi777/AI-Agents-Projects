import pytest
from app import HopEvidence,multi_hop_retrieve
def test_hops_and_dedup():
 calls=[]
 def search(q):
  calls.append(q); return [HopEvidence("s1","first")] if len(calls)==1 else [HopEvidence("s1","duplicate"),HopEvidence("s2","second")]
 r=multi_hop_retrieve("question",search,lambda q,e:"follow up",2); assert len(r)==2 and r[1].evidence[0].source_id=="s2" and calls==["question","follow up"]
def test_bounds():
 with pytest.raises(ValueError): multi_hop_retrieve("q",lambda q:[],lambda q,e:"",6)
