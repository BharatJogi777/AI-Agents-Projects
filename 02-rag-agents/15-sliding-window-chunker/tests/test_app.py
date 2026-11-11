import pytest
from app import sliding_windows
def test_overlap():
 w=sliding_windows("abcdefghij",6,2); assert [(x.start,x.end) for x in w]==[(0,6),(4,10)] and w[0].text[-2:]==w[1].text[:2]
def test_empty_and_invalid():
 assert sliding_windows("",5,1)==[]
 with pytest.raises(ValueError): sliding_windows("x",5,5)
