import pytest
from app.monitor import Snapshot,compare
def test_detects_change():
 assert compare(Snapshot("https://example.org","old","t1"),Snapshot("https://example.org","new","t2"))["changed"]
def test_same_content_unchanged():
 assert compare(Snapshot("https://example.org","same","t1"),Snapshot("https://example.org","same","t2"))["status"]=="unchanged"
def test_rejects_different_urls():
 with pytest.raises(ValueError): compare(Snapshot("https://a.example","x","t"),Snapshot("https://b.example","y","t"))
