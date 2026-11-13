import pytest
from app.memory_leak import investigate
def test_growth(): assert investigate([{"memory_mb":1},{"memory_mb":3},{"memory_mb":5}])["sustained_growth"]
def test_flat(): assert not investigate([{"memory_mb":5},{"memory_mb":5}])["sustained_growth"]
def test_empty():
 with pytest.raises(ValueError): investigate([])
