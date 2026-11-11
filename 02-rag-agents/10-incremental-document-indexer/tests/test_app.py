import pytest
from app import IncrementalIndexer
def test_skip_update_delete(tmp_path):
 i=IncrementalIndexer(tmp_path/"idx.db",100,10)
 try:
  text="a"*150; assert i.index("doc",text)=="indexed"; assert len(i.get_chunks("doc"))==2
  assert i.index("doc",text)=="unchanged"; assert i.index("doc","changed")=="indexed"
  assert len(i.get_chunks("doc"))==1 and i.delete("doc") and not i.get_chunks("doc") and not i.delete("doc")
 finally: i.close()
def test_validation(tmp_path):
 with pytest.raises(ValueError): IncrementalIndexer(tmp_path/"bad.db",100,100)
 i=IncrementalIndexer(tmp_path/"ok.db")
 try:
  with pytest.raises(ValueError): i.index("","x")
  with pytest.raises(TypeError): i.index("id",None)
 finally: i.close()
