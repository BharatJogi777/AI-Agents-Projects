import pytest
from app.drill import create_drill_plan

def test_builds_restore_drill_plan():
 r=create_drill_plan('region outage',rto_minutes=60,rpo_minutes=15,services=['api','db'])
 assert any('Restore' in p for p in r.phases) and len(r.safety_notes)>=2

def test_rejects_duplicate_services():
 with pytest.raises(ValueError): create_drill_plan('outage',rto_minutes=1,rpo_minutes=1,services=['api','api'])
