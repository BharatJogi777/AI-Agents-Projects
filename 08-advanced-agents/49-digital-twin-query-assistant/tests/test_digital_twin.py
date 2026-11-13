import pytest
from datetime import datetime,timezone,timedelta
from app.digital_twin import Observation, query_observations, summarize

def test_queries_only_matching_asset_and_time():
    now=datetime.now(timezone.utc)
    rows=[Observation("pump-1","pressure",2,"bar",now-timedelta(minutes=2)),Observation("pump-2","pressure",9,"bar",now)]
    result=query_observations(rows,asset_id="pump-1",metric="pressure",as_of=now)
    assert summarize(result)["average"]==2

def test_rejects_naive_as_of():
    with pytest.raises(ValueError):
        query_observations([],asset_id="pump",metric="temp",as_of=datetime(2026,1,1))
