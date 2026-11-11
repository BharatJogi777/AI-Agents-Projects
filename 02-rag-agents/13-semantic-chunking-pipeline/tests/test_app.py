import pytest
from app import semantic_chunks
def test_boundary():
 r=semantic_chunks("Alpha topic. More alpha. Completely different.",lambda a,b:.1 if "different" in b else .9,.5,5,100); assert len(r)==2 and r[0].start==0 and r[-1].text.endswith("different.")
def test_invalid():
 with pytest.raises(ValueError): semantic_chunks("x",lambda a,b:1,2)
