import pytest
from app.patent_landscape import summarize_patents
def test_aggregates_supplied_records():
 r=summarize_patents(records=[{"patent_id":"P1","status":"Granted","technology":"AI","filing_date":"2024"},{"patent_id":"P2","status":"Pending","technology":"AI"}])
 assert r.total_records==2 and dict(r.technology_counts)=={"AI":2} and r.records_missing_dates==("P2",)
def test_rejects_duplicate_ids():
 with pytest.raises(ValueError): summarize_patents(records=[{"patent_id":"P","status":"x","technology":"y"},{"patent_id":"P","status":"x","technology":"y"}])
