import pytest
from app.irrigation import FieldWaterStatus,advise_irrigation
def test_calculates_advisory_runtime():
 f=FieldWaterStatus("F1",2,20,40,10)
 r=advise_irrigation([f])
 assert r["fields"][0]["suggested_runtime_hours"]==2 and not r["irrigation_started"]
def test_rejects_invalid_moisture():
 with pytest.raises(ValueError): advise_irrigation([FieldWaterStatus("F",1,120,50,5)])
