import pytest
from memory_summarizer import MemorySummarizer
class Summarizer:
 def summarize(self,text):return "Explicit preference: concise answers."
def test_summary_metadata():
 result=MemorySummarizer(Summarizer()).summarize_with_metadata("conversation")
 assert result.text.startswith("Explicit") and result.source_chars==12
def test_source_and_output_limits():
 with pytest.raises(ValueError):MemorySummarizer(Summarizer(),2).summarize("long")
 class Large:
  def summarize(self,text):return "x"*20
 with pytest.raises(ValueError):MemorySummarizer(Large(),max_summary_chars=5).summarize("ok")
