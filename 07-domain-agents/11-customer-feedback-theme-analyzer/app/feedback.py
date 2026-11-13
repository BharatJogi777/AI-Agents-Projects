"""Deterministic feedback theme classification with traceable matched terms."""
from dataclasses import dataclass

THEMES={"usability":("confusing","difficult","easy to use","intuitive","navigation"),"performance":("slow","latency","crash","loading","timeout"),"pricing":("expensive","price","cost","billing","value"),"support":("support","agent","response","helpful","ticket"),"reliability":("outage","down","unavailable","broken","reliable")}
@dataclass(frozen=True)
class FeedbackAnalysis:
    themes: tuple[str,...]
    sentiment: str
    matched_terms: tuple[str,...]

def analyze_feedback(text: str) -> FeedbackAnalysis:
    if not isinstance(text,str) or not text.strip(): raise ValueError("feedback text is required")
    normalized=text.casefold(); found=[]; terms=[]
    for theme,keywords in THEMES.items():
        matches=[word for word in keywords if word in normalized]
        if matches: found.append(theme); terms.extend(matches)
    positive=sum(normalized.count(w) for w in ("great","good","excellent","love","easy","helpful","fast"))
    negative=sum(normalized.count(w) for w in ("bad","poor","hate","broken","slow","confusing","expensive","frustrating"))
    sentiment="positive" if positive>negative else "negative" if negative>positive else "mixed_or_neutral"
    return FeedbackAnalysis(tuple(found),sentiment,tuple(terms))
