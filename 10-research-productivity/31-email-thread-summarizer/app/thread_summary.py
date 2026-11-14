"""Summarize supplied email messages chronologically and extract open questions."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ThreadSummary:
    participants: tuple[str,...]
    message_count: int
    chronological_messages: tuple[str,...]
    open_questions: tuple[str,...]

def summarize_thread(*, messages: list[dict[str,str]]) -> ThreadSummary:
    if not isinstance(messages,list) or not messages: raise ValueError("messages must be a non-empty list")
    participants=set(); ordered=[]; questions=[]
    for m in messages:
        if not isinstance(m,dict) or not all(isinstance(m.get(k),str) and m[k].strip() for k in ("sender","timestamp","body")): raise ValueError("each message needs sender, timestamp and body")
        participants.add(m["sender"].strip())
        ordered.append((m["timestamp"],f'{m["timestamp"]} — {m["sender"]}: {m["body"].strip()}'))
        for line in m["body"].splitlines():
            text=line.strip()
            if text.endswith("?"): questions.append(text)
    ordered.sort(key=lambda x:x[0])
    return ThreadSummary(tuple(sorted(participants)),len(messages),tuple(x[1] for x in ordered),tuple(dict.fromkeys(questions)))
