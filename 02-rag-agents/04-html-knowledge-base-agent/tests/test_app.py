import pytest
from app import extract_html
def test_extract_content_only():
 d=extract_html('<title>Help</title><h1>Install</h1><p>Read <a href="/docs">docs</a></p><script>steal()</script><style>.x{}</style>')
 assert d.title=="Help" and "Install" in d.text and "steal" not in d.text and d.links==("/docs",)
def test_size_guard():
 with pytest.raises(ValueError): extract_html("x"*101,100)
