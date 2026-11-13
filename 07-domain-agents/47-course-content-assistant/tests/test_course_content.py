import pytest
from app.content import Lesson,prepare_lesson
def test_prepares_source_grounded_lesson_outline():
 l=Lesson("L1","Intro",("Explain concept",),("book:p10",),90)
 r=prepare_lesson(l,"beginner",45)
 assert r["estimated_minutes"]==45 and r["sources"]==["book:p10"] and r["educator_review_required"]
def test_requires_sources():
 with pytest.raises(ValueError): prepare_lesson(Lesson("L","Title",("Objective",),(),20),"beginner")
