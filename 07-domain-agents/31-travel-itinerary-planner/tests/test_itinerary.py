from datetime import date
import pytest
from app.itinerary import Stop,build_itinerary
def test_sorts_stops():
 r=build_itinerary([Stop(date(2026,2,1),600,660,"Museum"),Stop(date(2026,2,1),480,540,"Cafe")])
 assert r["stops"][0]["place"]=="Cafe" and not r["booking_performed"]
def test_rejects_overlap():
 with pytest.raises(ValueError): build_itinerary([Stop(date(2026,2,1),480,600,"A"),Stop(date(2026,2,1),590,650,"B")])
