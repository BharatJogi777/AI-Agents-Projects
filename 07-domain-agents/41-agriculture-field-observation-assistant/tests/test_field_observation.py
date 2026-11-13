from datetime import datetime
import pytest
from app.observations import Observation,review_observations
def test_prioritizes_high_severity_with_evidence():
 now=datetime(2026,5,2)
 x=Observation("O1","F1",now,"disease",5,"Leaf spots visible","photo-1")
 r=review_observations([x],now)
 assert r["observations"][0]["priority"]=="urgent_review" and r["observations"][0]["evidence_ref"]=="photo-1"
def test_rejects_future_observation():
 now=datetime(2026,5,2)
 with pytest.raises(ValueError): review_observations([Observation("O","F",datetime(2026,5,3),"water",1,"note","ref")],now)
