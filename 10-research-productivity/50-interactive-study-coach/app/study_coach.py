"""Evaluate supplied study answers and calculate simple review intervals."""
from dataclasses import dataclass
from datetime import date,timedelta
@dataclass(frozen=True)
class Flashcard:
    id:str; question:str; accepted_answers:tuple[str,...]
def evaluate_answer(card:Flashcard,answer:str,reviewed_on:date,previous_interval_days:int=0,streak:int=0)->dict:
    if not card.id.strip() or not card.question.strip() or not card.accepted_answers or any(not a.strip() for a in card.accepted_answers): raise ValueError("card needs an id, question, and non-empty accepted answers")
    if previous_interval_days<0 or streak<0: raise ValueError("interval and streak cannot be negative")
    if not answer.strip(): raise ValueError("answer is required")
    correct=answer.strip().casefold() in {a.strip().casefold() for a in card.accepted_answers}
    next_streak=streak+1 if correct else 0
    interval=max(1,previous_interval_days*2 if correct and previous_interval_days else 1) if correct else 1
    return {"card_id":card.id,"correct":correct,"streak":next_streak,"next_review":reviewed_on+timedelta(days=interval),"interval_days":interval,"feedback":"Correct" if correct else "Review the reference answer and try again."}
