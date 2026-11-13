from datetime import date
import pytest
from app.disruption import SupplyEvent,assess_events
def test_ranks_disruptions_with_sources():
 r=assess_events([SupplyEvent("E1","S1","chip",date(2026,1,1),5,5,"ticket-1")],date(2026,1,2))
 assert r["events"][0]["risk"]=="critical" and r["events"][0]["source_ref"]=="ticket-1"
def test_rejects_invalid_severity():
 with pytest.raises(ValueError): assess_events([SupplyEvent("E","S","C",date(2026,1,1),1,9,"ref")],date(2026,1,2))
