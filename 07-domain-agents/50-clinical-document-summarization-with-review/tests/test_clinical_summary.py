import pytest
from app.summary import ClinicalNote,prepare_review_packet
def test_builds_metadata_only_review_packet():
 n=ClinicalNote("D1","PAT-1","CLIN-1","2026-01-01",{"assessment":"Source note text"},("ehr:doc-1",))
 r=prepare_review_packet(n)
 assert r["section_inventory"][0]["section"]=="assessment" and r["clinician_review_required"] and not r["patient_facing_output_authorized"]
def test_requires_source_references():
 n=ClinicalNote("D","P","C","2026-01-01",{"note":"text"},())
 with pytest.raises(ValueError): prepare_review_packet(n)
