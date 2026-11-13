from datetime import date
import pytest
from app.evidence import Evidence, assess_evidence
def test_expired_and_pending():
 r=assess_evidence([Evidence("C1","drive://file",date(2026,1,1),date(2026,1,2)),Evidence("C2","ticket://2",date(2026,1,3))],date(2026,1,4))
 assert r["expired"]==1 and r["pending_review"]==1 and not r["certification"]
def test_duplicate_rejected():
 with pytest.raises(ValueError): assess_evidence([Evidence("C","a",date.today()),Evidence("C","b",date.today())])
