import pytest
from app.pagination import paginate

def test_page_metadata_and_offsets():
    values=list(range(7))
    first=paginate(values,limit=3)
    second=paginate(values,offset=3,limit=3)
    assert first.items==[0,1,2] and first.has_more and first.total==7
    assert second.items==[3,4,5] and second.has_more
    assert not paginate(values,offset=6,limit=3).has_more

@pytest.mark.parametrize("kwargs",[{"offset":-1},{"limit":0},{"limit":101},{"limit":2,"max_limit":0}])
def test_invalid_pagination(kwargs):
    with pytest.raises(ValueError):
        paginate([1,2],**kwargs)
