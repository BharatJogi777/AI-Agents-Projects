import pytest
from app.literature import Reference,search_literature
def test_returns_cited_matching_literature():
 r=Reference("R1","Tomato blight review","tomato",("fungal","blight"),"Review of management evidence.",2024,True)
 out=search_literature([r],"tomato","fungal blight")
 assert out["results"][0]["reference_id"]=="R1" and out["consult_local_agronomist"]
def test_abstains_without_matching_evidence():
 assert search_literature([],"maize","rust resistance")["answer_status"]=="insufficient_evidence"
def test_rejects_duplicate_reference():
 r=Reference("R","Title","maize",("rust",),"Summary",2020,True)
 with pytest.raises(ValueError): search_literature([r,r],"maize","rust")
