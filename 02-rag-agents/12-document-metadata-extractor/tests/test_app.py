import pytest
from app import extract_metadata
def test_metadata(tmp_path):
 p=tmp_path/"notes.txt"; p.write_text("hello"); m=extract_metadata(p); assert m.media_type=="text/plain" and m.size_bytes==5 and len(m.sha256)==64
def test_limits(tmp_path):
 p=tmp_path/"x.bin"; p.write_bytes(b"abc")
 with pytest.raises(ValueError): extract_metadata(p,2)
 with pytest.raises(ValueError): extract_metadata(tmp_path/"missing")
