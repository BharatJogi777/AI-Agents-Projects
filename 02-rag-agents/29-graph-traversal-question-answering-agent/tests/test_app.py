from app import Edge,find_paths
def test_path_and_provenance():
 p=find_paths("A","C",[Edge("A","knows","B","d1"),Edge("B","works_with","C","d2")]); assert p[0].nodes==("A","B","C") and p[0].evidence_ids==("d1","d2")
def test_cycle_and_hop_limit():
 edges=[Edge("A","to","B","1"),Edge("B","back","A","2"),Edge("B","to","C","3")]; assert find_paths("A","C",edges,1)==[] and len(find_paths("A","C",edges,2))==1
