import pytest
from app.market_research import summarize_market
def test_aggregates_segments_and_prices():
 r=summarize_market(observations=[{"segment":"SMB","market_size":10,"price":20},{"segment":"SMB","market_size":5,"price":30},{"segment":"Enterprise","market_size":7}])
 assert dict(r.segment_totals)=={"Enterprise":7.0,"SMB":15.0} and r.average_price==25
def test_rejects_negative_market_size():
 with pytest.raises(ValueError): summarize_market(observations=[{"segment":"A","market_size":-1}])
