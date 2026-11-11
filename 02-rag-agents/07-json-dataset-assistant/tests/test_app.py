import pytest
from app import parse_json_records
def test_paths_and_canonical_json():
 r=parse_json_records('[{"b":2,"a":1},{"x":"é"}]'); assert r[0].path=="$[0]" and r[0].canonical_json=='{"a":1,"b":2}' and r[1].path=="$[1]"
def test_reject_invalid_and_oversize():
 with pytest.raises(ValueError): parse_json_records("true")
 with pytest.raises(ValueError): parse_json_records('{"x":NaN}')
 with pytest.raises(ValueError): parse_json_records("{}",max_bytes=1)
