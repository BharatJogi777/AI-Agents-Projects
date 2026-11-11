from typing import Protocol
from .contracts import Summary
class Summarizer(Protocol):
    def summarize(self,text:str)->str: ...
class MemorySummarizer:
    def __init__(self,summarizer:Summarizer,max_source_chars:int=12000,max_summary_chars:int=1200):
        if type(max_source_chars) is not int or max_source_chars<1 or type(max_summary_chars) is not int or max_summary_chars<1:raise ValueError("limits must be positive integers")
        self.summarizer=summarizer;self.max_source_chars=max_source_chars;self.max_summary_chars=max_summary_chars
    def summarize(self,conversation:str)->str:
        return self.summarize_with_metadata(conversation).text
    def summarize_with_metadata(self,conversation:str)->Summary:
        if not isinstance(conversation,str) or not conversation.strip() or len(conversation)>self.max_source_chars:raise ValueError("source empty or too large")
        output=self.summarizer.summarize(conversation)
        if not isinstance(output,str) or not output.strip() or len(output)>self.max_summary_chars:raise ValueError("invalid or oversized summary")
        normalized=output.strip()
        return Summary(normalized,len(conversation),len(normalized))
