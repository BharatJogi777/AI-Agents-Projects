import pytest
from app.hypothesis_critique import critique_hypothesis
def test_complete_hypothesis_scores_well():
 r=critique_hypothesis(hypothesis="Caching reduces latency",population="API requests",variables=["cache","latency"],measurable_outcome="p95 ms",falsifiable_condition="p95 does not decrease")
 assert r.score==100 and not r.improvements and r.review_required
def test_missing_dimensions_are_reported():
 r=critique_hypothesis(hypothesis="",population="",variables=[],measurable_outcome="",falsifiable_condition="")
 assert r.score==0 and len(r.improvements)==5
def test_bad_variables_rejected():
 with pytest.raises(ValueError): critique_hypothesis(hypothesis="x",population="y",variables=[" "],measurable_outcome="z",falsifiable_condition="q")
