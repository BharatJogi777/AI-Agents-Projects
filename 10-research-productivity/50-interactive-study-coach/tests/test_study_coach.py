from app.study_coach import Flashcard,evaluate_answer
from datetime import date
import pytest
def test_correct_answer_increases_interval():
 card=Flashcard("1","What is an API?",("application programming interface",))
 r=evaluate_answer(card,"Application Programming Interface",date(2026,11,15),3,2)
 assert r["correct"] and r["streak"]==3 and r["interval_days"]==6
def test_wrong_answer_resets_streak():
 r=evaluate_answer(Flashcard("1","Q?",("yes",)),"no",date(2026,11,15),8,4)
 assert not r["correct"] and r["streak"]==0 and r["interval_days"]==1
def test_blank_answer_rejected():
 with pytest.raises(ValueError): evaluate_answer(Flashcard("1","Q?",("yes",))," ",date.today())
