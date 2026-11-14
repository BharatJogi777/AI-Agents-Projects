import pytest
from app.dataset_discovery import discover_datasets
def test_filters_catalogue_by_topics_and_formats():
 c=[{"dataset_id":"D1","topics":["climate","rainfall"],"formats":["csv"]},{"dataset_id":"D2","topics":["climate"],"formats":["json"]}]
 r=discover_datasets(catalogue=c,required_topics=["climate","rainfall"],required_formats=["csv"])
 assert [x.dataset_id for x in r]==["D1"]
def test_rejects_bad_catalogue_entry():
 with pytest.raises(ValueError): discover_datasets(catalogue=[{}],required_topics=["x"])
