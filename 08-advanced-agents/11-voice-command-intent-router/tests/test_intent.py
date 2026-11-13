import pytest
from app.intent import Intent,route_command
def test_exact_match_requires_confirmation():
 r=route_command("open dashboard",[Intent("open_dashboard",("open dashboard",))])
 assert r["intent"]=="open_dashboard" and r["requires_confirmation"] and not r["execute"]
def test_ambiguous_match_does_not_execute():
 r=route_command("start",[Intent("start_a",("start",)),Intent("start_b",("start",))])
 assert r["status"]=="ambiguous" and not r["execute"]
def test_empty_transcript_rejected():
 with pytest.raises(ValueError): route_command(" ",[])
