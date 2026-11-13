import pytest
from app.hotspots import investigate
def test_ranks_by_total_time():
 r=investigate([{"operation":"a","duration_ms":2},{"operation":"b","duration_ms":9},{"operation":"a","duration_ms":3}])
 assert r[0]["operation"]=="a" and r[0]["total_ms"]==5
def test_zero_total_share(): assert investigate([{"operation":"x","duration_ms":0}])[0]["share"]==0
def test_invalid_duration():
 with pytest.raises(ValueError): investigate([{"operation":"x","duration_ms":-1}])
