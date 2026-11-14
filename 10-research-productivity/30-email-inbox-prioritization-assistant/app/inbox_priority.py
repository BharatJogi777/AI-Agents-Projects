"""Prioritize supplied email metadata without opening or sending messages."""
from dataclasses import dataclass

@dataclass(frozen=True)
class EmailPriority:
    message_id: str
    score: int
    reasons: tuple[str,...]

def prioritize_inbox(*, messages: list[dict]) -> tuple[EmailPriority,...]:
    if not isinstance(messages,list): raise ValueError("messages must be a list")
    results=[]; seen=set()
    for msg in messages:
        if not isinstance(msg,dict) or not isinstance(msg.get("id"),str) or not msg["id"].strip(): raise ValueError("each message needs an ID")
        mid=msg["id"]
        if mid in seen: raise ValueError("message IDs must be unique")
        seen.add(mid)
        score=0; reasons=[]
        if msg.get("is_direct") is True: score+=3; reasons.append("directly addressed")
        if msg.get("is_starred") is True: score+=2; reasons.append("starred")
        if msg.get("has_deadline") is True: score+=4; reasons.append("deadline indicated")
        if msg.get("is_unread") is True: score+=1; reasons.append("unread")
        if msg.get("sender_is_vip") is True: score+=2; reasons.append("sender marked important")
        results.append(EmailPriority(mid,score,tuple(reasons)))
    return tuple(sorted(results,key=lambda x:(-x.score,x.message_id)))
