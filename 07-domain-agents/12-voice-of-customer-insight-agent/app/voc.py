"""Aggregate customer feedback into auditable theme counts."""
from collections import Counter
from dataclasses import dataclass
from .feedback import analyze_feedback

@dataclass(frozen=True)
class VoiceOfCustomerSummary:
    total_records: int
    theme_counts: tuple[tuple[str,int],...]
    sentiment_counts: tuple[tuple[str,int],...]
    source_ids: tuple[str,...]

def summarize_voice_of_customer(records: list[dict]) -> VoiceOfCustomerSummary:
    if not isinstance(records,list) or not records: raise ValueError("records must be a non-empty list")
    themes=Counter(); sentiments=Counter(); ids=[]
    for index,record in enumerate(records):
        if not isinstance(record,dict) or not isinstance(record.get("text"),str) or not record["text"].strip(): raise ValueError(f"record {index} requires non-empty text")
        sid=record.get("source_id",str(index+1))
        if not isinstance(sid,str) or not sid.strip(): raise ValueError(f"record {index} has invalid source_id")
        result=analyze_feedback(record["text"]); themes.update(result.themes); sentiments.update([result.sentiment]); ids.append(sid)
    return VoiceOfCustomerSummary(len(records),tuple(sorted(themes.items(),key=lambda x:(-x[1],x[0]))),tuple(sorted(sentiments.items())),tuple(ids))
