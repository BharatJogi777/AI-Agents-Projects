import pytest
from app.research import Source,build_research_brief,validate_source
def test_brief_keeps_provenance():
 s=Source("https://docs.example.org/a","Docs","Quoted fact","2026-01-01")
 assert build_research_brief("What changed?",[s],{"docs.example.org"})["sources"][0]["url"]==s.url
def test_rejects_untrusted_host():
 with pytest.raises(ValueError): validate_source(Source("https://evil.example","x","y","now"),{"docs.example.org"})
