import pytest
from app.research_gaps import find_research_gaps
def test_finds_missing_dimensions():
 r=find_research_gaps(required_dimensions=["cost","latency","security"],observed_dimensions=["latency","cost"])
 assert r.missing_dimensions==("security",) and r.coverage_ratio==pytest.approx(2/3)
def test_rejects_empty_required_set():
 with pytest.raises(ValueError): find_research_gaps(required_dimensions=[],observed_dimensions=[])
