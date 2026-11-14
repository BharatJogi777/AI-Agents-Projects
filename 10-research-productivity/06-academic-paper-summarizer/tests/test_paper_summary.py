import pytest
from app.paper_summary import summarize_paper
def test_summary_preserves_supplied_sections():
 r=summarize_paper(source_id="P1",abstract="Aim",methods="RCT",findings="Improved",limitations="Small cohort")
 assert r.objective=="Aim" and r.methods=="RCT" and r.source_id=="P1"
 assert r.open_questions
def test_rejects_missing_section():
 with pytest.raises(ValueError):
  summarize_paper(source_id="P1",abstract="Aim",methods=" ",findings="x",limitations="y")
