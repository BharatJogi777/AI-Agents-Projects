from datetime import datetime
def prepare(topic: str, start: datetime, end: datetime, attendees: list[str], agenda: list[str], context: list[dict] | None = None) -> dict:
    if not topic.strip(): raise ValueError("topic is required")
    if end<=start: raise ValueError("meeting end must be after start")
    people=sorted({x.strip() for x in attendees if x.strip()},key=str.casefold)
    if not people: raise ValueError("at least one attendee is required")
    if not agenda or any(not x.strip() for x in agenda): raise ValueError("agenda items must be non-empty")
    refs=[]
    for item in context or []:
        if not item.get("source") or not item.get("summary"): raise ValueError("context items require source and summary")
        refs.append({"source":item["source"],"summary":item["summary"]})
    return {"topic":topic.strip(),"start":start.isoformat(),"end":end.isoformat(),"attendees":people,"agenda":[x.strip() for x in agenda],"context":refs,"decisions_prejudged":False}
