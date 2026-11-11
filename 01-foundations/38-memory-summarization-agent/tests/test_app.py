import pytest
from app import *
class S:
 def summarize(self,t):return "Explicit preference: concise answers."
def test_summary():assert MemorySummarizer(S()).summarize("chat").startswith("Explicit")
def test_source_limit():
 with pytest.raises(ValueError):MemorySummarizer(S(),2).summarize("long")
def test_output_limit():
 class B:
  def summarize(self,t):return "x"*20
 with pytest.raises(ValueError):MemorySummarizer(B(),max_summary_chars=5).summarize("ok")
