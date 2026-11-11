import pytest
from app import ingest
def test_text_and_json(tmp_path):
 p=tmp_path/"n.md"; p.write_text("# Hi"); assert ingest(p)[0].text=="# Hi"
 j=tmp_path/"d.json"; j.write_text('[{"a":1},{"b":2}]'); rows=ingest(j); assert len(rows)==2 and rows[1].metadata["record"]==1
def test_extension_and_size(tmp_path):
 p=tmp_path/"x.bin"; p.write_bytes(b"abc")
 with pytest.raises(ValueError): ingest(p)
 with pytest.raises(ValueError): ingest(p,max_bytes=2)
