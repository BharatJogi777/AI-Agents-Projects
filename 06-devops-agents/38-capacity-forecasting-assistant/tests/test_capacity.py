from app.capacity import forecast_capacity
import pytest

def test_forecasts_threshold_date():
    result=forecast_capacity([{"resource":"cpu","day":0,"utilization_percent":50},{"resource":"cpu","day":10,"utilization_percent":70}],threshold_percent=80)
    assert result[0].days_to_threshold==5

def test_rejects_duplicate_day():
    with pytest.raises(ValueError): forecast_capacity([{"resource":"x","day":1,"utilization_percent":20},{"resource":"x","day":1,"utilization_percent":30}])
