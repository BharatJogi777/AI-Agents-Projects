import pytest
from app.chart import Datum,interpret_chart
def test_computes_summary():
 r=interpret_chart("Revenue","USD",[Datum("Q1",2),Datum("Q2",5)])
 assert r["total"]==7 and r["maximum"]["label"]=="Q2"
def test_rejects_duplicate_labels():
 with pytest.raises(ValueError): interpret_chart("x","u",[Datum("A",1),Datum("A",2)])
def test_requires_data():
 with pytest.raises(ValueError): interpret_chart("x","u",[])
