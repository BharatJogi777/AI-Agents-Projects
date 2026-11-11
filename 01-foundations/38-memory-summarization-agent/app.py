from typing import Protocol
class Summarizer(Protocol):
 def summarize(self,text:str)->str:...
class MemorySummarizer:
 def __init__(self,summarizer,max_source_chars=12000,max_summary_chars=1200):
  self.summarizer=summarizer;self.max_source_chars=max_source_chars;self.max_summary_chars=max_summary_chars
 def summarize(self,conversation):
  if not conversation.strip() or len(conversation)>self.max_source_chars:raise ValueError("source empty or too large")
  out=self.summarizer.summarize(conversation)
  if not isinstance(out,str) or not out.strip() or len(out)>self.max_summary_chars:raise ValueError("invalid or oversized summary")
  return out.strip()
